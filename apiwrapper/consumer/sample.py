from . import ConsumerApiWrapper
import requests


class SampleWrapper(ConsumerApiWrapper):
    def __init__(self, tokenstr):
        super().__init__(tokenstr)

    def get_samples(self, serial, starttime, endtime, offset=0, limit=None):
        samplesurl = "{consumerapiurl}/samples".format(consumerapiurl=self.consumerapiurl)

        payload = {
            'serial': serial,
            'starttimestr': starttime,
            'endtimestr': endtime,
            'offset': offset
        }

        if limit is not None:
            payload['limit'] = limit


        # Using urlencode is important to remove the '+' and convert it to %2B. Date decode does
        # not work without it.
        r = requests.get(samplesurl, params=payload)
        ConsumerApiWrapper.process_status(r.status_code)
        sample_response = r.json()
        return sample_response