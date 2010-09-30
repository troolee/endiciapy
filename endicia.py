from logging import debug
from io import StringIO
import urllib2
import urllib

from serialization import to_xml
from response import EndiciaResponse
from endiciapy.enums import ImageFormat, ImageRotation, ImageResolution,\
    LabelSize, LabelType, NonDeliveryOption


class Endicia(object):
    def __init__(self, requester_id, account_id, pass_phrase, 
                 url='https://www.envmgr.com/LabelService/EwsLabelService.asmx', 
                 test_mode=False, format_xml=False):
        self.url = url.strip('/')
        self.requester_id = requester_id
        self.account_id = account_id
        self.pass_phrase = pass_phrase
        self.test_mode = test_mode
        self.format_xml = format_xml


    def get_account_status(self):
        res = self.__post('GetAccountStatusXML', accountStatusRequestXML={
            'AccountStatusRequest': {
                'RequesterID': self.requester_id,
                'RequestID': 'GAS12345',
                'CertifiedIntermediary': {
                    'AccountID': self.account_id,
                    'PassPhrase': self.pass_phrase,
                },
            },
        })
        return res


    def get_postage_label(self, weight, mail_class, partner_customer_id, partner_transaction_id, 
                          frm, to, return_address, type=LabelType.Default, size=LabelSize._4x6, 
                          image_format=ImageFormat.PNG, image_resolution=ImageResolution._300, 
                          image_rotation=ImageRotation._None, date_advance=0, mailpiece_shape=None,
                          mailpiece_dimensions=None, automation_rate=None, machinable=None,
                          service_level=None, sunday_holiday_delivery=None, sort_type=None,
                          include_postage=None, reply_postage=None, show_return_address=None,
                          stealth=None, validate_address=None, signature_waiver=None,
                          no_weekend_delivery=None, services=None, tracking_number=None,
                          cost_center=None, value=None, insured_value=None, cod_amount=None,
                          description=None, customs_form_type=None, customs_form_image_format=None,
                          customs_form_image_resolution=None, origin_country=None, contents_type=None,
                          non_delivery_option=NonDeliveryOption.Return, contents_explanation=None,
                          reference_id=None, bpod_client_duns_number=None, rubber_stamp=None,
                          entry_facility=None, po_zip_code=None, ship_date=None, ship_time=None,
                          eel_pfc=None, customs_certify=None, customs_signer=None, response_options=None,
                          postage_price=None, no_holiday_delivery=None, return_to_sender=None,
                          barcode_format=None):

        assert(not response_options) # TODO: Need to be implemented
        
        mailpiece_dimensions = mailpiece_dimensions and {
            'Length': mailpiece_dimensions[0],
            'Width': mailpiece_dimensions[1],
            'Height': mailpiece_dimensions[2],
        }
        
        labelRequest = {
            '_': {
                'LabelType': type,
                'LabelSize': size,
                'ImageFormat': image_format,
                'ImageResolution': image_resolution,
                'ImageRotation': image_rotation,
            },
            'RequesterID': self.requester_id,
            'AccountID': self.account_id,
            'PassPhrase': self.pass_phrase,
            'WeightOz': weight,
            'MailClass': mail_class,
            'NonDeliveryOption': non_delivery_option,
            'PartnerCustomerID': partner_customer_id,
            'PartnerTransactionID': partner_transaction_id, 
        }
        if self.test_mode:
            labelRequest['_']['Test'] = 'YES'
            
        def put(k, p, container=None):
            container = labelRequest if container is None else container
            if p is not None: container[k] = p
            return container
        put('DateAdvance', date_advance)
        put('MailpieceShape', mailpiece_shape)
        put('MailpieceDimensions', mailpiece_dimensions)
        put('AutomationRate', self.__to_bool(automation_rate))
        put('Machinable', self.__to_bool(machinable))
        put('ServiceLevel', service_level)
        put('SundayHolidayDelivery', self.__to_bool(sunday_holiday_delivery))
        put('SortType', sort_type)
        put('IncludePostage', self.__to_bool(include_postage))
        put('ReplyPostage', self.__to_bool(reply_postage))
        put('ShowReturnAddress', self.__to_bool(show_return_address))
        put('Stealth', self.__to_bool(stealth))
        put('ValidateAddress', self.__to_bool(validate_address))
        put('SignatureWaiver', self.__to_bool(signature_waiver))
        put('NoWeekendDelivery', self.__to_bool(no_weekend_delivery))
        put('TrackingNumber', tracking_number)
        put('CostCenter', cost_center)
        put('Value', value)
        put('InsuredValue', insured_value)
        put('CODAmount', cod_amount)
        put('Description', description)
        put('CustomsFormType', customs_form_type)
        put('CustomsFormImageFormat', customs_form_image_format)
        put('CustomsFormImageResolution', customs_form_image_resolution)
        put('OriginCountry', origin_country)
        put('ContentsType', contents_type)
        put('ContentsExplanation', contents_explanation)
        put('ReferenceID', reference_id)
        put('BpodClientDunsNumber', bpod_client_duns_number)
        put('EntryFacility', entry_facility)
        put('POZipCode', po_zip_code)
        put('ShipDate', ship_date)
        put('ShipTime', ship_time)
        put('EelPfc', eel_pfc)
        put('CustomsCertify', customs_certify)
        put('CustomsSigner', customs_signer)
        put('ResponseOptions', postage_price and {'_': {'PostagePrice': self.__to_bool(postage_price)}})
        put('NoHolidayDelivery', self.__to_bool(no_holiday_delivery))
        put('ReturntoSender', self.__to_bool(return_to_sender))
        put('BarcodeFormat', barcode_format)

        if rubber_stamp:
            rubber_stamp = rubber_stamp.split('\n')
            rubber_stamp = rubber_stamp + [None]*(3-len(rubber_stamp))
            for i in range(1, 4):
                put('RubberStamp%d' % i, rubber_stamp[i - 1])
                
        def put_complex(prefix, struct, required, optionals):
            for k, p in required:
                labelRequest[prefix+k] = struct[p]
                del struct[p]
            for k, p in optionals:
                if p in struct:
                    put(prefix+k, struct[p])
                    del struct[p]
            assert(len(struct) == 0)
                
        put_complex('From', frm, 
                    required=[
                        ('City', 'city'),
                        ('State', 'state'),
                        ('PostalCode', 'postal_code'),],
                    optionals=[
                        ('Name', 'name'),
                        ('Company', 'company'),
                        ('ZIP4', 'zip4'),
                        ('Country', 'country'),
                        ('Phone', 'phone'),
                        ('EMail', 'email'),])
        put_complex('To', to, 
                    required=[
                        ('Address1', 'address1'),
                        ('City', 'city'),
                        ('State', 'state'),
                        ('PostalCode', 'postal_code'),],
                    optionals=[
                        ('Name', 'name'),
                        ('Company', 'company'),
                        ('Address2', 'address2'),
                        ('Address3', 'address3'),
                        ('Address4', 'address4'),
                        ('ZIP4', 'zip4'),
                        ('DeliveryPoint', 'delivery_point'),
                        ('Country', 'country'),
                        ('Phone', 'phone'),
                        ('EMail', 'email'),])
        if isinstance(return_address, (list, tuple)):
            return_address = list(isinstance) + [None] * (4 - len(return_address))
            return_address = return_address[:4]
        else:
            return_address = [return_address, None, None, None]
        for i in range(1, 5):
            put('ReturnAddress%d' % i, return_address[i - 1])
          
        if services is not None:
            def _get(k):
                v = services.get(k)
                if v is None: return None
                return 'ON' if v else 'OFF' 
            services_attrs = {}
            services_attrs = put('CertifiedMail', _get('certified_mail'), services_attrs)    
            services_attrs = put('COD', _get('cod'), services_attrs)
            services_attrs = put('DeliveryConfirmation', _get('delivery_confirmation'), services_attrs)
            services_attrs = put('ElectronicReturnReceipt', _get('electronic_return_receipt'), services_attrs)
            services_attrs = put('InsuredMail', services.get('insured_mail'), services_attrs) 
            services_attrs = put('RestrictedDelivery', _get('restricted_delivery'), services_attrs) 
            services_attrs = put('ReturnReceipt', _get('return_receipt'), services_attrs) 
            services_attrs = put('SignatureConfirmation', _get('signature_confirmation'), services_attrs)
            labelRequest['Services'] = {'_': services_attrs, }
        
#        debug(pformat(labelRequest))
        res = self.__post('GetPostageLabelXML', labelRequestXML={
            'LabelRequest': labelRequest,
        })
        return res


    def recredit_request(self, recredit_amount, request_id='BP123'):
        res = self.__post('BuyPostageXML', recreditRequestXML={
            'RecreditRequest': {
                'RequesterID': self.requester_id,
                'RequestID': request_id,
                'CertifiedIntermediary': {
                    'AccountID': self.account_id,
                    'PassPhrase': self.pass_phrase,
                },
                'RecreditAmount': recredit_amount,
            },
        })
        return res


    def change_pass_phrase(self, new_pass_phrase, request_id='CPP123'):
        res = self.__post('ChangePassPhraseXML', changePassPhraseRequestXML={
            'ChangePassPhraseRequest': {
                'RequesterID': self.requester_id,
                'RequestID': request_id,
                'CertifiedIntermediary': {
                    'AccountID': self.account_id,
                    'PassPhrase': self.pass_phrase,
                },
                'NewPassPhrase': new_pass_phrase,
            },
        })
        return res
    
    
    def status_request(self, *pic_numbers):
        pic_numbers = map(lambda x: {'PICNumber': x}, pic_numbers)
        res = self.__post2('StatusRequest', XMLInput={
            'StatusRequest': {
                'AccountID': self.account_id,
                'Test': 'Y' if self.test_mode else 'N',
                'PassPhrase': self.pass_phrase,
                'StatusList': pic_numbers,
            } 
        })
        return res


    def __post(self, method, debug_mode=False, **data):
        url = '/'.join((self.url, method))
        key, xml = data.keys()[0], StringIO()
        to_xml(xml, data[key], format=self.format_xml)
        data = (key, xml.getvalue())
        if debug_mode: debug('\n%s', data[1])
        data = urllib.urlencode((data, ))
        try:
            response = urllib2.urlopen(url, data).read()
            return EndiciaResponse(response)
        except urllib2.HTTPError, e:
            debug(e)
            return None
        
    def __post2(self, method, debug_mode=False, **data):
        url = 'https://www.endicia.com/ELS/ELSServices.cfc'
        key, xml = data.keys()[0], StringIO()
        to_xml(xml, data[key], format=self.format_xml)
        data = (key, xml.getvalue())
        if debug_mode: debug('\n%s', data[1])
        data = urllib.urlencode((('Method', method), data))
        if debug_mode: debug(data)
        try:
            response = urllib2.urlopen(url, data).read()
            return EndiciaResponse(response)
        except urllib2.HTTPError, e:
            debug(e)
            return None
    
    def __to_bool(self, v):
        if v is None: return None
        return 'TRUE' if v else 'FALSE'
