import {getAuthUrl} from './tools'

let config = {
  qiniuDomain: 'http://pbuuzdjec.bkt.clouddn.com/'
}

if (process.env.NODE_ENV === 'development') {
  config = {
    ...config,
    origin: 'test_api',
    db: 'jd30new',
    accountCode: 'fnt',
    code: null,
    url: getAuthUrl(),
    jsApiList: ['biz.contact.complexPicker', 'biz.util.scan', 'device.geolocation.get'],
    agentId: 181941774
  }
} else if (process.env.NODE_ENV === 'production') {
  config = {
    ...config,
    origin: 'http://xian.jd.funenc.com',
    db: 'jd_v2_production',
    accountCode: '001',
    code: null,
    url: getAuthUrl(),
    jsApiList: ['biz.contact.complexPicker', 'biz.util.scan', 'device.geolocation.get'],
    agentId: 182893994
    // origin: 'http://172.16.109.53:8069',
    // db: 'jd30new',
    // accountCode: 'fnt',
    // code: null,
    // url: getAuthUrl(),
    // jsApiList: ['biz.contact.complexPicker', 'biz.util.scan', 'device.geolocation.get'],
    // agentId: 181433366
  }
}
console.log(config)
export default config
