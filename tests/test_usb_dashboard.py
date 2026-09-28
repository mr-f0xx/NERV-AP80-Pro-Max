"""Static USB skin/asset checks, not a firmware parser or device simulation."""
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / '.rockbox/wps/NERV_AP80.sbs').read_text()
USB = TEXT.split('#__USB\n')[1]
ASSETS = ROOT / '.rockbox/wps/NERV_AP80'


class UsbDashboard(unittest.TestCase):
    def test_usb_routing_and_menu_title_visibility(self):
        self.assertIn('%?if(%cs, =, 21)<%VI(clearScreen)%Vd(usb)|%VI(menuViewport)%Vd(info)>', TEXT)
        self.assertIn('%Vi(clearScreen,0,0,1,1,-)', TEXT)
        self.assertIn('%Vi(menuViewport,16,80,328,470,5)', TEXT)
        self.assertIn('%Vl(info,72,22,150,30,3)', TEXT)
        self.assertEqual(re.findall(r'%V\([^\n]+\)', TEXT), ['%V(0,0,360,1,-)'])

    def test_usb_viewports_stay_inside_screen(self):
        viewports = re.findall(r'%Vl\(([^,]+),(\d+),(\d+),(\d+),(\d+),([^)]*)\)', USB)
        self.assertGreater(len(viewports), 20)
        for label, x, y, w, h, font in viewports:
            self.assertEqual(label, 'usb')
            x, y, w, h = map(int, (x,y,w,h))
            self.assertGreater(w, 0)
            self.assertGreater(h, 0)
            self.assertLessEqual(x+w, 360)
            self.assertLessEqual(y+h, 640)
            if font != '-':
                size = {'2':15,'3':18,'4':22,'5':29,'6':35}[font]
                raw = (ROOT/f'.rockbox/fonts/{size}-KodeMonoMPlus2-SemiBold.fnt').read_bytes()
                self.assertLessEqual(struct.unpack_from('<H',raw,6)[0], h)

    def test_assets_and_noninteractive_gauge(self):
        for name,label in [('charge_fill.bmp','ChargeFill'),('charge_back.bmp','ChargeBack')]:
            raw=(ASSETS/name).read_bytes()
            self.assertEqual(raw[:2], b'BM')
            self.assertEqual(struct.unpack_from('<ii',raw,18),(272,60))
            self.assertEqual(struct.unpack_from('<H',raw,28)[0],24)
            self.assertIn(f'%xl({label},{name},0,0)',TEXT)
        self.assertIn('%bl(0,0,272,60,ChargeFill,backdrop,ChargeBack,horizontal,notouch)',USB)
        self.assertNotIn('%T(',USB)

    def test_charge_status_does_not_confuse_external_power_with_charging(self):
        self.assertIn('%?bc<CHARGING|%?if(%bl, =, 100)<BATTERY FULL|%?bp<EXTERNAL POWER|USB CONNECTED>>>',USB)
        self.assertNotIn('%?bp<CHARGING',USB)
        self.assertIn('%?bp<EXTERNAL|USB LINK>',USB)

    def test_unknown_readings_and_clock_fallback(self):
        self.assertIn('%?if(%bl, >=, 0)<%bl%%|--%%>',USB)
        self.assertIn('%?if(%bl, >=, 0)<%bl(0,0,272,60,ChargeFill,backdrop,ChargeBack,horizontal,notouch)|%xd(ChargeBack)>',USB)
        self.assertIn('%?if(%bv, =, ?)<-- V|%bv V>',USB)
        self.assertIn('%?cc<%cH:%cM|--:-->',USB)
        self.assertIn('%?cc<%cY-%cm-%cd|NO RTC>',USB)
        self.assertNotIn('%bt',USB)  # runtime estimate is not a charge ETA

    def test_text_samples_fit_bundled_fonts(self):
        def width(text,size):
            raw=(ROOT/f'.rockbox/fonts/{size}-KodeMonoMPlus2-SemiBold.fnt').read_bytes()
            _,_,_,_,_,first,_,_,bits,offsets,nwidth = struct.unpack_from('<4sHHHHIIIIII',raw)
            start=((36+bits+3)&~3)+offsets*4
            widths=raw[start:start+nwidth]
            return sum(widths[ord(c)-first] for c in text)
        for text,size,w in [
            ('NERV // POWER',22,272),('AP80 PRO MAX / USB',15,272),
            ('100%',35,328),('--%',35,328),('USB CONNECTED',18,328),
            ('CHARGING',22,328),('BATTERY FULL',22,328),('EXTERNAL POWER',22,328),
            ('USB CONNECTED',22,328),('BATTERY STATUS / LIVE',15,328),
            ('BATTERY VOLTAGE',15,160),('4.08 V',22,132),('-- V',22,132),
            ('POWER INPUT',15,108),('EXTERNAL',22,188),('USB LINK',22,188),
            ('DEVICE TIME',15,140),('23:59',22,136),('--:--',22,136),
            ('2026-09-28',15,136),('NO RTC',15,136),
            ('EJECT ON HOST',15,328),('BEFORE DISCONNECTING',15,328),
        ]:
            self.assertLessEqual(width(text,size),w,text)

    def test_card_text_uses_card_background(self):
        cards=USB.split('# Telemetry cards:')[1].split('# Static safety reminder')[0]
        text_views=re.findall(r'%Vl\(usb,[^\n]+,[23456]\)\n(%Vf\([^\n]+\)\n%Vb\([^\n]+\))',cards)
        self.assertEqual(len(text_views),7)
        for styles in text_views:
            self.assertIn('%Vb(100A18)',styles)


if __name__ == '__main__':
    unittest.main()
