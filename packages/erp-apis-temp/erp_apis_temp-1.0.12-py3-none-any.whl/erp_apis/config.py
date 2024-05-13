# coding: utf-8
# Project：erp_out_of_stock
# File：config.py
# Author：李福成
# Date ：2024-04-29 10:04
# IDE：PyCharm

Erp321BaseUrl = 'https://www.erp321.com'
ErpApiBaseUrl = 'https://api.erp321.com'



DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/237.84.2.178 Safari/537.36 Edg/109.0.1518.78',
    'cookie': 'acw_tc=2760779b17154951601776467e2eaae3707f13160901b36135bd350c5c0636; _ati=2632320813015; j_d_3=3ZEUHZ3LD6TF2GRXTWSSJ6LVEZIAKQE7XTZO5II3AI23TRQYIQ2RLBFPPHLVXCO7YVXQXAL36AGJ2C5RQMV7RAGT74; u_ssi=; u_drp=; u_r=12%2c13%2c14%2c15%2c17%2c18%2c22%2c23%2c27%2c28%2c29%2c30%2c31%2c32%2c33%2c34%2c35%2c36%2c39%2c40%2c41%2c52%2c53%2c54%2c61%2c62%2c101%2c1001%2c109; u_shop=-1; u_lastLoginType=ap; tfstk=fP2koMDya7lSpJ-dr-D53zgD_v1xFUMI1ypKJv3FgquXyUp8YpcUADiE4k77-J0qUXN-J43nKkaGDNBOBuZSdx7OWOIUOX6jd2WKLiurgfDFWNBxX-cS2vPd8MOQmoujxUuETyWqgqir4vurTERqbquELvze0Iotb2orT4-qMARrWJPa3GEdPKE0TP2mqb5Y4qJEc-moZVrzEpJUb0co7uucWF37yjrItJtBKfEz1yiazU7tNkP0o0DhHQkamWzic8W9rmN80ygqgHJQmX0ug8lDYpr4m4cgtzbkN4P8ofiqgHXsDP34V8PcAErzW4Dr0jBNjolUM8G_eZJoQ5Z-eWzC6IMuY7kc4fO2_so6dmSLnBOIamim5gRoxaMJO6PPmiATAbojfVIcmBMjamimUijD1DlrccyC.; 3AB9D23F7A4B3C9B=3ZEUHZ3LD6TF2GRXTWSSJ6LVEZIAKQE7XTZO5II3AI23TRQYIQ2RLBFPPHLVXCO7YVXQXAL36AGJ2C5RQMV7RAGT74; u_name=%e6%9d%8e%e7%a6%8f%e6%88%90; u_lid=18986680202; u_json=%7b%22t%22%3a%222024-5-12+14%3a49%3a03%22%2c%22co_type%22%3a%22%e6%a0%87%e5%87%86%e5%95%86%e5%ae%b6%22%2c%22proxy%22%3anull%2c%22ug_id%22%3a%2211003725%22%2c%22dbc%22%3a%221149%22%2c%22tt%22%3a%2295%22%2c%22apps%22%3a%221.4.7.150.152.168.169%22%2c%22pwd_valid%22%3a%220%22%2c%22ssi%22%3anull%2c%22sign%22%3a%224001967.1EA70FE2D4EB480D859D91A98D86E11F%2cd566f976b2c825e4ca410ee0754bcf2b%22%7d; u_co_name=%e6%ad%a6%e6%b1%89%e5%b0%8f%e5%b8%83%e7%94%b5%e5%ad%90%e5%95%86%e5%8a%a1%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8; v_d_144=1715496538498_f488932826196e289944b013be36a727; u_cid=133599701439643594; u_sso_token=CS@e1903f92c5c7459fbbe381ba85d75c00; u_id=15424700; u_co_id=10174711; p_50=5DA09A8DA5EF6EC4DE5BE6D6A0231599638511221439646836%7c10174711; u_env=www'
}
'''
  //生成唯一SessionCode
  if (!$.cookie('SessionCode')) {
    let guid = newJstTraceGuid();
    $.cookie('SessionCode', guid);
    params.SessionCode = guid;
  }


'''