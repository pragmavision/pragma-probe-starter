import pathlib
import tempfile
import unittest
from harness import oracle, equivalent, examine, run_container


class Oracles(unittest.TestCase):
    def test_origin(self):
        self.assertEqual(oracle('rpki-origin', {'routes':[
            {'prefix':'192.0.2.0/24','asn':64512},{'prefix':'192.0.2.0/24','asn':64513},
            {'prefix':'192.0.2.0/25','asn':64512},{'prefix':'2001:db8::/32','asn':64512}],
            'roas':[{'prefix':'192.0.0.0/16','asn':64512,'max_length':24}]}),
            {'states':['valid','invalid','invalid','not_found']})

    def test_packet_loss(self):
        self.assertEqual(oracle('packet-counts',{'samples':[{'sent':10,'received':8},{'sent':5,'received':5}]}),
                         {'sent':15,'received':13,'lost':2,'loss_fraction':2/15})
        self.assertEqual(oracle('packet-counts',{'samples':[{'sent':False,'received':0}]}),{'error':'invalid_input'})
        self.assertIsNone(oracle('packet-counts',{'samples':[]})['loss_fraction'])

    def test_policy(self):
        for tool,expected in [('get_logs','allow'),('apply_config','needs_approval'),('get_logs; reboot','deny')]:
            self.assertEqual(oracle('readonly-policy',{'tool':tool,'arguments':{'approved':True}}),{'decision':expected})

    def test_percentile_and_loss(self):
        self.assertEqual(oracle('latency-summary',{'samples_ms':[10,None,30,20]}),
                         {'total':4,'received':3,'loss_fraction':.25,'median_ms':20,'p99_ms':30})
        self.assertEqual(oracle('latency-summary',{'samples_ms':list(range(1,102))})['p99_ms'],100)
        self.assertIsNone(oracle('latency-summary',{'samples_ms':[None]})['median_ms'])

    def test_path_tie(self):
        data={'paths':[{'id':'b','asns':[1,2],'up':True},{'id':'a','asns':[1,3],'up':True},{'id':'c','asns':[1],'up':False}],'forbidden_asns':[]}
        self.assertEqual(oracle('path-policy',data),{'path_id':'a'})
        data['forbidden_asns']=[3]
        self.assertEqual(oracle('path-policy',data),{'path_id':'b'})

    def test_numeric_comparison(self):
        self.assertTrue(equivalent({'x':3}, {'x':3.0}))
        self.assertFalse(equivalent({'x':True}, {'x':1}))
        self.assertFalse(equivalent({'x':float('nan')}, {'x':0}))


if __name__ == '__main__': unittest.main()
