class LabelType:
    Default = 'Default'
    CertifiedMail = 'CertifiedMail'
    DestinationConfirm = 'DestinationConfirm'  
    International = 'International'
    
    
class LabelSize:
    _4x6 = '4X6'
    _4x5 = '4X5'
    _4x4_5 = '4X4.5'
    _6x4 = '6X4'
    _7x3 = '7X3'
    _7x4 = '7X4'
    _8x3 = '8X3'
    DocTab = 'DocTab'
    Dymo30384 = 'Dymo30384'
    EnvelopeSize10 = 'EnvelopeSize10'
    Mailer7x5 = 'Mailer7x5'
    Booklet = 'Booklet'
    

class ImageFormat:
    EPL2 = 'EPL2'
    GIF = 'GIF'
    JPEG = 'JPEG'
    PDF = 'PDF'
    PNG = 'PNG'
    ZPLII = 'ZPLII'


class ImageResolution:
    _150 = '150'
    _203 = '203'
    _300 = '300'
    

class ImageRotation:
    _None = 'None'
    Rotate90 = 'Rotate90'
    Rotate180 = 'Rotate180'
    Rotate270 = 'Rotate270'


class MailClass:
    Express = 'Express'
    First = 'First'
    LibraryMail = 'LibraryMail'
    MediaMail = 'MediaMail'
    ParcelPost = 'ParcelPost'
    ParcelSelect = 'ParcelSelect'
    Priority = 'Priority'
    StandardMail = 'StandardMail'
    ExpressMailInternational = 'ExpressMailInternational' 
    FirstClassMailInternational = 'FirstClassMailInternational' 
    PriorityMailInternational = 'PriorityMailInternational' 


class MailpieceShape:
    Card = 'Card'
    Letter = 'Letter'
    Flat = 'Flat'
    Parcel = 'Parcel'
    LargeParcel = 'LargeParcel'
    IrregularParcel = 'IrregularParcel'
    OversizedParcel = 'OversizedParcel'
    FlatRateEnvelope = 'FlatRateEnvelope'
    FlatRatePaddedEnvelope = 'FlatRatePaddedEnvelope'
    SmallFlatRateBox = 'SmallFlatRateBox'
    MediumFlatRateBox = 'MediumFlatRateBox'
    LargeFlatRateBox = 'LargeFlatRateBox'


class ServiceLevel:
    NextDay2ndDayPOToAddressee = 'NextDay2ndDayPOToAddressee'


class SortType:
    BMC = 'BMC'
    FiveDigit = 'FiveDigit'
    MixedBMC = 'MixedBMC'
    Nonpresorted = 'Nonpresorted'
    Presorted = 'Presorted'
    SCF = 'SCF'
    SinglePiece = 'SinglePiece'
    ThreeDigit = 'ThreeDigit'
    

class TrackingNumber:
    _22 = '22'
    _14 = '14'
    _12 = '12'


class CustomsFormType:
    _None = 'None'
    Form2976 = 'Form2976'
    Form2976A = 'Form2976A' 


class CustomsFormImageFormat:
    GIF = 'GIF'
    JPEG = 'JPEG'
    PDF = 'PDF'
    PNG = 'PNG'
    
    
class CustomsFormImageResolution:
    _150 = '150'
    _300 = '300'


class ContentsType:
    Documents = 'Documents'
    Gift = 'Gift'
    Merchandise = 'Merchandise'
    Other = 'Other'
    ReturnedGoods = 'ReturnedGoods'
    Sample = 'Sample'


class NonDeliveryOption:
    Return = 'Return'
    Abandon = 'Abandon'
    
    
class EntryFacility:
    DBMC = 'DBMC'
    DDU = 'DDU'
    DSCF = 'DSCF'
    OBMC = 'OBMC'
    Other = 'Other'


class InsuredMail:
    ON = 'ON'
    OFF = 'OFF'
    UspsOnline = 'UspsOnline'
    Endicia = 'Endicia'

class BarcodeFormat:
    PlanetCode14 = 'PLATNET Code, 14'
