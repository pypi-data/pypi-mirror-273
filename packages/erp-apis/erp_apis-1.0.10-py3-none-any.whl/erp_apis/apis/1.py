import requests

cookies = {
    '_ati': '5025820500865',
    'u_lastLoginType': 'ap',
    'u_env': 'www',
    'u_env_next': 'w',
    '3AB9D23F7A4B3C9B': 'ZYEPF7VW7LUOR23CAGNCY66FEL2X6QKARYRE6Z6P2IYTEYFIE4F2U3JBMJJKV7MIFL3POFPEQADEUSNNZDO5JJD7QE',
    'u_name': '%e5%90%b4%e6%b5%a9',
    'u_lid': '17671271393',
    'j_d_3': 'ZYEPF7VW7LUOR23CAGNCY66FEL2X6QKARYRE6Z6P2IYTEYFIE4F2U3JBMJJKV7MIFL3POFPEQADEUSNNZDO5JJD7QE',
    'u_ssi': '',
    'u_co_name': '%e6%ad%a6%e6%b1%89%e5%b0%8f%e5%b8%83%e7%94%b5%e5%ad%90%e5%95%86%e5%8a%a1%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8',
    'u_drp': '-1',
    'v_d_144': '1714791921793_2bdf86302ecbf586ad8809643a2c7da7',
    'u_cid': '133592655330850842',
    'u_r': '12%2c13%2c14%2c15%2c17%2c18%2c22%2c23%2c27%2c28%2c29%2c30%2c31%2c32%2c33%2c34%2c35%2c36%2c39%2c40%2c41%2c52%2c53%2c54%2c61%2c62%2c101',
    'u_sso_token': 'CS@96573de3a68140d89d1390346e29ff0e',
    'u_id': '18683738',
    'u_shop': '-1',
    'u_co_id': '10174711',
    'p_50': '126C1FA6A6A264FE507FCC9880AC9A62638504175330853959%7c10174711',
    'SessionCode': '3af4bac4-89df-79d4-1efa18f5113a645',
    'order_filter18683738': 'sl_.oql_.sl_agreement.bml_.rl_.date_arrow.iteml_.tl_.referr_.sourceStore_.other_-wor_co_id_to__.ssl_.nodesl_.ofl_.presend_head.icl_.labels_title.st_.p_shops_title.drp_co_id_tos_title.drp_co_id_froms_title.ll_.rl__.l_status_label.wh_.lwh_.asl__.customer_',
    'combine_show': 'true',
    'ss_u_env': 'pf',
    'ckv': '%7B%22itemsku_defaultFillQtyReturns%22%3Atrue%7D',
    '_batchItemTypeCookie': 'sku_id',
    'jt.pagesize': '.-Q1LCJU._500',
    'dkv': '%7B%22pstol_item%22%3A%22300%2C-5%22%2C%22pstorder_editor%22%3A%2225%2C-25%22%2C%22pstoe_item%22%3A%220%2C0%22%7D',
    'u_json': '%7b%22t%22%3a%222024-5-9+17%3a26%3a11%22%2c%22co_type%22%3a%22%e6%a0%87%e5%87%86%e5%95%86%e5%ae%b6%22%2c%22proxy%22%3anull%2c%22ug_id%22%3a%22%22%2c%22dbc%22%3a%221149%22%2c%22tt%22%3a%2295%22%2c%22apps%22%3a%221.4.7.150.152.168.169%22%2c%22pwd_valid%22%3a%220%22%2c%22ssi%22%3a%22%22%2c%22sign%22%3a%223998203.AB5752E30DC544FB8891021DD56899C2%2c3c0b51fcc1e74dd188e74dac22885629%22%7d',
    'aftersale_filter18683738': 'amount_io.dates_io.itemsku_type_io.api_down_oi.shops_io.exceptionl_.sl_.goodsl_.notify_status.aftertypesl_.aftershoptypesl_.order_type_io.order_status_io.shop_status_io.refund_status_io.drp_co_id_froms_io.drp_submit_io.suppliers_io.suppliers_submit_io.drp_process_status_io.drp_refund_status_io.question_type_io.as_label_io.label_io.result_type_io.node_io.wmss_io.order_wms_io.whs_io.l_id_search_title-labels_title',
    'AftersaleDefaultWh_18683738': '0',
    'acw_tc': '2760779b17153263430278398e2eb23bbae049144d33e3638479c3013d9571',
    'tfstk': 'f2Km6rcpQE7bAC2ti3jj4FqDzXuJXiIFbSAO61pN_tf5gSEYDUqMIdrVQZJNsCARNCbsh1CNsCpwkYnKvK9ffGSi9DndqkvmPIVauGkaz9BMP9QNIK9ff8Z6WO8JhPX8WSkGbCSzaO6db-Sw_arPC_rVQoWaaYX1a1SN_GPr496_grWN_bD8b6xwV3kp09auiBNTGxQVTK52HF-zY64fp_qab3Ylo6oAZlrwqtv5IDV8xVCeRsQdTQo8mGvPIQbpoXqDsdJB7axggxdeaFANFUGgS6YwHetRyRz2Ehfc8n7unxsRjORNSUG3vtjvrwxDlANy3BCD8i9TKjpl-UbCUayguiLpph_e0mVCww6MZwLmtoAF4rUz8u9UfTk9qPa1uT6lOxzcIjTIZ9ViEY4pCZW5d6HoEPa1uT6l9YDuJE_VF91d.',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ati=5025820500865; u_lastLoginType=ap; u_env=www; u_env_next=w; 3AB9D23F7A4B3C9B=ZYEPF7VW7LUOR23CAGNCY66FEL2X6QKARYRE6Z6P2IYTEYFIE4F2U3JBMJJKV7MIFL3POFPEQADEUSNNZDO5JJD7QE; u_name=%e5%90%b4%e6%b5%a9; u_lid=17671271393; j_d_3=ZYEPF7VW7LUOR23CAGNCY66FEL2X6QKARYRE6Z6P2IYTEYFIE4F2U3JBMJJKV7MIFL3POFPEQADEUSNNZDO5JJD7QE; u_ssi=; u_co_name=%e6%ad%a6%e6%b1%89%e5%b0%8f%e5%b8%83%e7%94%b5%e5%ad%90%e5%95%86%e5%8a%a1%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8; u_drp=-1; v_d_144=1714791921793_2bdf86302ecbf586ad8809643a2c7da7; u_cid=133592655330850842; u_r=12%2c13%2c14%2c15%2c17%2c18%2c22%2c23%2c27%2c28%2c29%2c30%2c31%2c32%2c33%2c34%2c35%2c36%2c39%2c40%2c41%2c52%2c53%2c54%2c61%2c62%2c101; u_sso_token=CS@96573de3a68140d89d1390346e29ff0e; u_id=18683738; u_shop=-1; u_co_id=10174711; p_50=126C1FA6A6A264FE507FCC9880AC9A62638504175330853959%7c10174711; SessionCode=3af4bac4-89df-79d4-1efa18f5113a645; order_filter18683738=sl_.oql_.sl_agreement.bml_.rl_.date_arrow.iteml_.tl_.referr_.sourceStore_.other_-wor_co_id_to__.ssl_.nodesl_.ofl_.presend_head.icl_.labels_title.st_.p_shops_title.drp_co_id_tos_title.drp_co_id_froms_title.ll_.rl__.l_status_label.wh_.lwh_.asl__.customer_; combine_show=true; ss_u_env=pf; ckv=%7B%22itemsku_defaultFillQtyReturns%22%3Atrue%7D; _batchItemTypeCookie=sku_id; jt.pagesize=.-Q1LCJU._500; dkv=%7B%22pstol_item%22%3A%22300%2C-5%22%2C%22pstorder_editor%22%3A%2225%2C-25%22%2C%22pstoe_item%22%3A%220%2C0%22%7D; u_json=%7b%22t%22%3a%222024-5-9+17%3a26%3a11%22%2c%22co_type%22%3a%22%e6%a0%87%e5%87%86%e5%95%86%e5%ae%b6%22%2c%22proxy%22%3anull%2c%22ug_id%22%3a%22%22%2c%22dbc%22%3a%221149%22%2c%22tt%22%3a%2295%22%2c%22apps%22%3a%221.4.7.150.152.168.169%22%2c%22pwd_valid%22%3a%220%22%2c%22ssi%22%3a%22%22%2c%22sign%22%3a%223998203.AB5752E30DC544FB8891021DD56899C2%2c3c0b51fcc1e74dd188e74dac22885629%22%7d; aftersale_filter18683738=amount_io.dates_io.itemsku_type_io.api_down_oi.shops_io.exceptionl_.sl_.goodsl_.notify_status.aftertypesl_.aftershoptypesl_.order_type_io.order_status_io.shop_status_io.refund_status_io.drp_co_id_froms_io.drp_submit_io.suppliers_io.suppliers_submit_io.drp_process_status_io.drp_refund_status_io.question_type_io.as_label_io.label_io.result_type_io.node_io.wmss_io.order_wms_io.whs_io.l_id_search_title-labels_title; AftersaleDefaultWh_18683738=0; acw_tc=2760779b17153263430278398e2eb23bbae049144d33e3638479c3013d9571; tfstk=f2Km6rcpQE7bAC2ti3jj4FqDzXuJXiIFbSAO61pN_tf5gSEYDUqMIdrVQZJNsCARNCbsh1CNsCpwkYnKvK9ffGSi9DndqkvmPIVauGkaz9BMP9QNIK9ff8Z6WO8JhPX8WSkGbCSzaO6db-Sw_arPC_rVQoWaaYX1a1SN_GPr496_grWN_bD8b6xwV3kp09auiBNTGxQVTK52HF-zY64fp_qab3Ylo6oAZlrwqtv5IDV8xVCeRsQdTQo8mGvPIQbpoXqDsdJB7axggxdeaFANFUGgS6YwHetRyRz2Ehfc8n7unxsRjORNSUG3vtjvrwxDlANy3BCD8i9TKjpl-UbCUayguiLpph_e0mVCww6MZwLmtoAF4rUz8u9UfTk9qPa1uT6lOxzcIjTIZ9ViEY4pCZW5d6HoEPa1uT6l9YDuJE_VF91d.',
    'origin': 'https://www.erp321.com',
    'priority': 'u=1, i',
    'referer': 'https://www.erp321.com/app/Service/aftersale/aftersale.aspx?_c=jst-epaas&owner_co_id=10174711&authorize_co_id=10174711',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

params = {
    '_c': 'jst-epaas',
    'owner_co_id': '10174711',
    'authorize_co_id': '10174711',
    'ts___': '1715327570664',
    'am___': 'Save',
}

data = '__VIEWSTATE=%2FwEPDwUKLTE1MzQyMDk2M2RkWyChnWSS0stgku0LK%2FKs2XXQMpw%3D&__VIEWSTATEGENERATOR=79B4B6F4&owner_co_id=10174711&authorize_co_id=10174711&_jt_page_count_enabled=&_jt_page_size=500&isCB=0&feedback=&__CALLBACKID=JTable1&__CALLBACKPARAM=%7B%22Method%22%3A%22Save%22%2C%22Args%22%3A%5B%22%7B%5C%22id%5C%22%3A%5C%22%5C%22%2C%5C%22as_id%5C%22%3A%5C%221452574341%5C%22%2C%5C%22owner_co_id%5C%22%3A%5C%220%5C%22%2C%5C%22o_id%5C%22%3A39568693%2C%5C%22as_date%5C%22%3A%5C%222024-05-10%2012%3A34%3A35%5C%22%2C%5C%22shop_type%5C%22%3A%5C%22%E4%BB%85%E9%80%80%E6%AC%BE%5C%22%2C%5C%22type%5C%22%3A%5C%22%E6%99%AE%E9%80%9A%E9%80%80%E8%B4%A7%5C%22%2C%5C%22status%5C%22%3A%5C%22%E5%BE%85%E7%A1%AE%E8%AE%A4%5C%22%2C%5C%22shop_status%5C%22%3A%5C%22%E9%80%80%E6%AC%BE%E6%88%90%E5%8A%9F%5C%22%2C%5C%22good_status%5C%22%3A%5C%22%E4%B9%B0%E5%AE%B6%E6%9C%AA%E6%94%B6%E5%88%B0%E8%B4%A7%5C%22%2C%5C%22shop_buyer_id%5C%22%3A%5C%22%E5%BC%A0**%5C%22%2C%5C%22shop_buyer_id_en%5C%22%3A%5C%22%E5%BC%A0**%5C%22%2C%5C%22receiver_mobile%5C%22%3A%5C%22********335%5C%22%2C%5C%22wms_id%5C%22%3A%5C%22%5C%22%2C%5C%22wh_id%5C%22%3A%5C%222%5C%22%2C%5C%22wh_code%5C%22%3A%5C%22%E6%AD%A6%E6%B1%89%E5%B0%8F%E5%B8%83%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E9%94%80%E9%80%80%E4%BB%93%5C%22%2C%5C%22warehouse%5C%22%3A%5C%22%E6%AD%A6%E6%B1%89%E5%B0%8F%E5%B8%83%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E9%94%80%E9%80%80%E4%BB%93%5C%22%2C%5C%22logistics_company%5C%22%3A%5C%22%E4%B8%AD%E9%80%9A%E9%80%9F%E9%80%92%5C%22%2C%5C%22l_id%5C%22%3A%5C%2278795429301452%5C%22%2C%5C%22refund_Qty%5C%22%3A1%2C%5C%22r_qty%5C%22%3A0%2C%5C%22buyer_apply_refund%5C%22%3A%5C%2225.98%5C%22%2C%5C%22shop_refund%5C%22%3A%5C%2225.98%5C%22%2C%5C%22shop_freight%5C%22%3A0%2C%5C%22back_amount%5C%22%3A25.98%2C%5C%22real_free_amount%5C%22%3A0%2C%5C%22urefund%5C%22%3A%5C%220%5C%22%2C%5C%22freight%5C%22%3A%5C%220%5C%22%2C%5C%22exchangeamount%5C%22%3A0%2C%5C%22upayment%5C%22%3A%5C%220%5C%22%2C%5C%22total_amount%5C%22%3A%5C%2225.98%5C%22%2C%5C%22refund_total_amount%5C%22%3A%5C%220%5C%22%2C%5C%22shop_name%5C%22%3A%5C%22TW-%E9%BB%91%E7%99%BD%E7%94%BA%E6%97%97%E8%88%B0%E5%BA%97%5C%22%2C%5C%22receiver_name%5C%22%3A%5C%22%E9%83%AD**%5C%22%2C%5C%22buyer_account%5C%22%3A%5C%22%5C%22%2C%5C%22seller_account%5C%22%3A%5C%22%5C%22%2C%5C%22question_type%5C%22%3A%5C%22%E6%8B%8D%E9%94%99%2F%E5%A4%9A%E6%8B%8D%2F%E4%B8%8D%E5%96%9C%E6%AC%A2%5C%22%2C%5C%22question_reason%5C%22%3A%5C%22%5C%22%2C%5C%22remark%5C%22%3A%5C%22%5C%22%2C%5C%22result%5C%22%3A%5C%22%5C%22%2C%5C%22advance_status%5C%22%3A%5C%22%E6%9C%AA%E7%94%B3%E8%AF%B7%E7%8A%B6%E6%80%81%5C%22%2C%5C%22exception_type%5C%22%3A%5C%22%5C%22%2C%5C%22drp_process_status%5C%22%3A%5C%22%5C%22%2C%5C%22drp_refund_status%5C%22%3A%5C%22%5C%22%2C%5C%22drp_co_id_from%5C%22%3A%5C%22%5C%22%2C%5C%22drp_co_id_to%5C%22%3A%5C%22%5C%22%2C%5C%22drp_submit2%5C%22%3Afalse%2C%5C%22drp_submit3%5C%22%3Afalse%2C%5C%22node%5C%22%3A%5C%22%E9%97%AE%E9%A2%98%E7%B1%BB%E5%9E%8B%E4%B8%8D%E5%AD%98%E5%9C%A8%5C%22%2C%5C%22so_id%5C%22%3A%5C%222145522542889300386%5C%22%2C%5C%22order_status%5C%22%3A%5C%22%E5%B7%B2%E5%8F%91%E8%B4%A7%5C%22%2C%5C%22order_type%5C%22%3A%5C%22%E6%99%AE%E9%80%9A%E8%AE%A2%E5%8D%95%5C%22%2C%5C%22order_remark%5C%22%3A%5C%22%5C%22%2C%5C%22order_paid_amount%5C%22%3A25.98%2C%5C%22order_labels%5C%22%3A%5C%22%E5%8F%91%E8%B4%A7%E5%90%8E%E5%8F%96%E6%B6%88%2C%E5%8F%91%E8%B4%A7%E5%90%8E%E5%94%AE%E5%90%8E%5C%22%2C%5C%22order_buyer_message%5C%22%3A%5C%22%5C%22%2C%5C%22order_creator_name%5C%22%3A%5C%22%5C%22%2C%5C%22hav_gift%5C%22%3A%5C%22%E6%97%A0%5C%22%2C%5C%22order_date%5C%22%3A%5C%222024-05-09%2007%3A11%3A04%5C%22%2C%5C%22pay_date%5C%22%3A%5C%222024-05-09%2007%3A11%3A15%5C%22%2C%5C%22modified%5C%22%3A%5C%222024-05-10%2015%3A46%3A51%5C%22%2C%5C%22confirm_date%5C%22%3A%5C%222024-05-10%2015%3A45%3A44%5C%22%2C%5C%22modifier_name%5C%22%3A%5C%22%E6%9D%8E%E7%A6%8F%E6%88%90%5C%22%2C%5C%22creator_name%5C%22%3A%5C%22%5C%22%2C%5C%22created%5C%22%3A%5C%222024-05-10%2012%3A34%3A38%5C%22%2C%5C%22send_date%5C%22%3A%5C%222024-05-09%2009%3A57%3A49%5C%22%2C%5C%22shop_end_date%5C%22%3A%5C%22%5C%22%2C%5C%22order_wms_id%5C%22%3A%5C%22%E6%AD%A6%E6%B1%89%E5%B0%8F%E5%B8%83%E7%94%B5%E5%AD%90%E5%95%86%E5%8A%A1%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%5C%22%2C%5C%22outer_as_id%5C%22%3A%5C%22155554647843308603%5C%22%2C%5C%22tag%5C%22%3A%5C%22%5C%22%2C%5C%22seller_flag%5C%22%3A%5C%22%5C%22%2C%5C%22refund_version%5C%22%3A1715315675272%2C%5C%22shop_site%5C%22%3A%5C%22%E6%B7%98%E5%AE%9D%E5%A4%A9%E7%8C%AB%5C%22%2C%5C%22co_id%5C%22%3A10174711%2C%5C%22shop_id%5C%22%3A10269548%2C%5C%22receiver_name_en%5C%22%3A%5C%22%E9%83%AD**%5C%22%2C%5C%22wms_co_id%5C%22%3A0%2C%5C%22deial_wh_id%5C%22%3A2%2C%5C%22notify_status%5C%22%3A%5C%22%5C%22%2C%5C%22is_split%5C%22%3A%5C%22%5C%22%2C%5C%22is_merge%5C%22%3A%5C%22%5C%22%2C%5C%22currency%5C%22%3A%5C%22%5C%22%2C%5C%22raw_so_id%5C%22%3A%5C%222145522542889300386%5C%22%2C%5C%22refund%5C%22%3A%5C%2225.98%5C%22%2C%5C%22payment%5C%22%3A%5C%220%5C%22%2C%5C%22labels%5C%22%3A%5C%22%5C%22%2C%5C%22tpw_to2%5C%22%3A0%2C%5C%22tpw_from2%5C%22%3A0%2C%5C%22oaid%5C%22%3A%5C%221kM4TDrw5eHBPhXPOEynuesDH1X1YDr2zwV7LfHxt6YNTe7P07rQmkynC9EHKymCfG4ia6IY%5C%22%2C%5C%22order_l_id%5C%22%3A%5C%2278795429301452%5C%22%2C%5C%22open_id%5C%22%3A%5C%22AAEW8-dTABsHV6KE1Lwv_C5H%5C%22%2C%5C%22is_cross_order%5C%22%3A%5C%220%5C%22%2C%5C%22free_amount%5C%22%3A0%2C%5C%22wms_outer_id%5C%22%3A%5C%22%5C%22%2C%5C%22tpw_to%5C%22%3A%5C%22%5C%22%2C%5C%22order_node%5C%22%3A%5C%22%5C%22%2C%5C%22__KeyData%5C%22%3A%5C%22r6K2PMCg9TXhgHHooHTJiqjEJhfNOuTMtWKNDqV5X1oQbvmTYLBS%2FE08g7uQrBcJ%5C%22%7D%22%5D%7D&__EVENTVALIDATION=%2FwEdAAJlnOVI9dne8YUaDTDzBxUIZcYKoPLGrxyB2M7KwGWMYZb8FLDIqA92sbTOfxQB052v3uTF'

response = requests.post(
    'https://www.erp321.com/app/Service/aftersale/aftersale.aspx',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.text)