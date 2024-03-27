import frappe
from hkm.erpnext___custom.po_approval.workflow_action import (
    get_allowed_options,
    get_workflow_action_url,
    get_confirm_workflow_action_url,
)


def get_approval_link(doc, user, allowed_options):
    if "Recommend" in allowed_options:
        return get_confirm_workflow_action_url(doc, "Recommend", user)
    if "First Approve" in allowed_options:
        return get_confirm_workflow_action_url(doc, "First Approve", user)
    if "Final Approve" in allowed_options:
        return get_confirm_workflow_action_url(doc, "Final Approve", user)
    else:
        frappe.throw(
            "Next ALM User is not allowed to approve the Document. Please ask for permission."
        )


def get_rejection_link(doc, user):
    return get_confirm_workflow_action_url(doc, "Reject", user)


def message_str(doc, user):
    allowed_options = get_allowed_options(user, doc)
    approval_link = get_approval_link(doc, user, allowed_options)
    rejection_link = get_rejection_link(doc, user)
    message = """
				<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
				<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
				<head>
				<!--[if gte mso 9]>
				<xml>
				  <o:OfficeDocumentSettings>
				    <o:AllowPNG/>
				    <o:PixelsPerInch>96</o:PixelsPerInch>
				  </o:OfficeDocumentSettings>
				</xml>
				<![endif]-->
				  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
				  <meta name="viewport" content="width=device-width, initial-scale=1.0">
				  <meta name="x-apple-disable-message-reformatting">
				  <!--[if !mso]><!--><meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
				  <title></title>
				  
				  <style type="text/css">
				      @media only screen and (min-width: 620px) {{
				  .u-row {{
				    width: 600px !important;
				  }}
				  .u-row .u-col {{
				    vertical-align: top;
				  }}

				  .u-row .u-col-16p5 {{
				    width: 99px !important;
				  }}

				  .u-row .u-col-16p67 {{
				    width: 100.02000000000002px !important;
				  }}

				  .u-row .u-col-18p66 {{
				    width: 111.96px !important;
				  }}

				  .u-row .u-col-19p5 {{
				    width: 117px !important;
				  }}

				  .u-row .u-col-20 {{
				    width: 120px !important;
				  }}

				  .u-row .u-col-31p67 {{
				    width: 190.02px !important;
				  }}

				  .u-row .u-col-32p29 {{
				    width: 193.74px !important;
				  }}

				  .u-row .u-col-32p39 {{
				    width: 194.34px !important;
				  }}

				  .u-row .u-col-32p88 {{
				    width: 197.28px !important;
				  }}

				  .u-row .u-col-33p33 {{
				    width: 199.98px !important;
				  }}

				  .u-row .u-col-33p56 {{
				    width: 201.36px !important;
				  }}

				  .u-row .u-col-35 {{
				    width: 210px !important;
				  }}

				  .u-row .u-col-44p84 {{
				    width: 269.04px !important;
				  }}

				  .u-row .u-col-45p17 {{
				    width: 271.02px !important;
				  }}

				  .u-row .u-col-67p61 {{
				    width: 405.66px !important;
				  }}

				  .u-row .u-col-67p71 {{
				    width: 406.25999999999993px !important;
				  }}

				  .u-row .u-col-100 {{
				    width: 600px !important;
				  }}

				}}

				@media (max-width: 620px) {{
				  .u-row-container {{
				    max-width: 100% !important;
				    padding-left: 0px !important;
				    padding-right: 0px !important;
				  }}
				  .u-row .u-col {{
				    min-width: 320px !important;
				    max-width: 100% !important;
				    display: block !important;
				  }}
				  .u-row {{
				    width: calc(100% - 40px) !important;
				  }}
				  .u-col {{
				    width: 100% !important;
				  }}
				  .u-col > div {{
				    margin: 0 auto;
				  }}
				  .no-stack .u-col {{
				    min-width: 0 !important;
				    display: table-cell !important;
				  }}

				  .no-stack .u-col-16p5 {{
				    width: 16.5% !important;
				  }}

				  .no-stack .u-col-16p67 {{
				    width: 16.67% !important;
				  }}

				  .no-stack .u-col-18p66 {{
				    width: 18.66% !important;
				  }}

				  .no-stack .u-col-19p5 {{
				    width: 19.5% !important;
				  }}

				  .no-stack .u-col-20 {{
				    width: 20% !important;
				  }}

				  .no-stack .u-col-31p67 {{
				    width: 31.67% !important;
				  }}

				  .no-stack .u-col-32p29 {{
				    width: 32.29% !important;
				  }}

				  .no-stack .u-col-32p39 {{
				    width: 32.39% !important;
				  }}

				  .no-stack .u-col-32p88 {{
				    width: 32.88% !important;
				  }}

				  .no-stack .u-col-33p33 {{
				    width: 33.33% !important;
				  }}

				  .no-stack .u-col-33p56 {{
				    width: 33.56% !important;
				  }}

				  .no-stack .u-col-35 {{
				    width: 35% !important;
				  }}

				  .no-stack .u-col-44p84 {{
				    width: 44.84% !important;
				  }}

				  .no-stack .u-col-45p17 {{
				    width: 45.17% !important;
				  }}

				  .no-stack .u-col-67p61 {{
				    width: 67.61% !important;
				  }}

				  .no-stack .u-col-67p71 {{
				    width: 67.71% !important;
				  }}

				}}
				body {{
				  margin: 0;
				  padding: 0;
				}}

				table,
				tr,
				td {{
				  vertical-align: top;
				  border-collapse: collapse;
				}}

				p {{
				  margin: 0;
				}}

				.ie-container table,
				.mso-container table {{
				  table-layout: fixed;
				}}

				* {{
				  line-height: inherit;
				}}

				a[x-apple-data-detectors='true'] {{
				  color: inherit !important;
				  text-decoration: none !important;
				}}

				table, td {{ color: #000000; }} a {{ color: #0000ee; text-decoration: underline; }} @media (max-width: 480px) {{ #u_row_16 .v-row-background-color {{ background-color: #ffffff !important; }} #u_row_16.v-row-background-color {{ background-color: #ffffff !important; }} #u_content_image_4 .v-container-padding-padding {{ padding: 20px 5px 5px !important; }} #u_content_image_4 .v-src-width {{ width: auto !important; }} #u_content_image_4 .v-src-max-width {{ max-width: 25% !important; }} #u_content_heading_87 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_87 .v-text-align {{ text-align: center !important; }} #u_content_heading_2 .v-container-padding-padding {{ padding: 11px 10px 24px !important; }} #u_content_heading_2 .v-font-size {{ font-size: 10px !important; }} #u_content_image_5 .v-container-padding-padding {{ padding: 20px 5px 5px !important; }} #u_content_image_5 .v-src-width {{ width: auto !important; }} #u_content_image_5 .v-src-max-width {{ max-width: 25% !important; }} #u_content_heading_88 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_88 .v-text-align {{ text-align: center !important; }} #u_content_heading_3 .v-container-padding-padding {{ padding: 20px 7px 36px 14px !important; }} #u_content_heading_3 .v-font-size {{ font-size: 12px !important; }} #u_content_image_6 .v-container-padding-padding {{ padding: 21px 5px 5px !important; }} #u_content_image_6 .v-src-width {{ width: auto !important; }} #u_content_image_6 .v-src-max-width {{ max-width: 28% !important; }} #u_content_heading_89 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_89 .v-text-align {{ text-align: center !important; }} #u_content_heading_4 .v-container-padding-padding {{ padding: 19px 10px 31px !important; }} #u_content_heading_4 .v-font-size {{ font-size: 15px !important; }} #u_row_52 .v-row-background-color {{ background-color: #ffffff !important; }} #u_row_52.v-row-background-color {{ background-color: #ffffff !important; }} #u_row_36 .v-row-background-color {{ background-color: #ffffff !important; }} #u_row_36.v-row-background-color {{ background-color: #ffffff !important; }} #u_content_image_12 .v-container-padding-padding {{ padding: 20px 5px 5px !important; }} #u_content_image_12 .v-src-width {{ width: auto !important; }} #u_content_image_12 .v-src-max-width {{ max-width: 26% !important; }} #u_content_heading_90 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_90 .v-text-align {{ text-align: center !important; }} #u_content_image_13 .v-container-padding-padding {{ padding: 20px 5px 5px !important; }} #u_content_image_13 .v-src-width {{ width: auto !important; }} #u_content_image_13 .v-src-max-width {{ max-width: 25% !important; }} #u_content_heading_91 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_91 .v-text-align {{ text-align: center !important; }} #u_content_heading_35 .v-container-padding-padding {{ padding: 10px 10px 39px !important; }} #u_content_image_14 .v-container-padding-padding {{ padding: 21px 5px 5px !important; }} #u_content_image_14 .v-src-width {{ width: auto !important; }} #u_content_image_14 .v-src-max-width {{ max-width: 26% !important; }} #u_content_heading_92 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_92 .v-text-align {{ text-align: center !important; }} #u_content_heading_36 .v-container-padding-padding {{ padding: 14px 10px 39px !important; }} #u_column_121 .v-col-background-color {{ background-color: #fcfcfc !important; }} #u_content_heading_67 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_67 .v-font-size {{ font-size: 12px !important; }} #u_content_heading_68 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_68 .v-font-size {{ font-size: 12px !important; }} #u_content_heading_69 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_69 .v-font-size {{ font-size: 12px !important; }} #u_content_heading_70 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_70 .v-font-size {{ font-size: 12px !important; }} #u_content_heading_72 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_73 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_73 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_74 .v-container-padding-padding {{ padding: 40px 2px 39px !important; }} #u_content_heading_74 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_75 .v-container-padding-padding {{ padding: 40px 2px 39px !important; }} #u_content_heading_75 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_93 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_94 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_95 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_96 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_97 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_98 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_99 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_100 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_101 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_102 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_103 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_content_heading_104 .v-container-padding-padding {{ padding: 40px 10px 39px !important; }} #u_row_37 .v-row-columns-background-color-background-color {{ background-color: #ffffff !important; }} #u_row_37.v-row-padding--vertical {{ padding-top: 0px !important; padding-bottom: 0px !important; }} #u_content_heading_37 .v-container-padding-padding {{ padding: 33px 3px 12px 22px !important; }} #u_content_heading_37 .v-font-size {{ font-size: 14px !important; }} #u_content_heading_66 .v-container-padding-padding {{ padding: 20px 10px 19px 9px !important; }} #u_row_35 .v-row-columns-background-color-background-color {{ background-color: #ffffff !important; }} #u_content_heading_31 .v-container-padding-padding {{ padding: 20px 10px 12px 22px !important; }} #u_content_heading_15 .v-container-padding-padding {{ padding: 20px 10px !important; }} #u_content_heading_25 .v-font-size {{ font-size: 12px !important; }} #u_content_heading_105 .v-font-size {{ font-size: 15px !important; }} #u_content_heading_105 .v-line-height {{ line-height: 100% !important; }} #u_row_19 .v-row-columns-background-color-background-color {{ background-color: #ffffff !important; }} #u_content_heading_5 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_5 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_6 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_6 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_7 .v-container-padding-padding {{ padding: 10px !important; }} #u_content_heading_7 .v-font-size {{ font-size: 10px !important; }} #u_row_24 .v-row-columns-background-color-background-color {{ background-color: #faf9f9 !important; }} #u_content_heading_22 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_22 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_77 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_77 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_76 .v-container-padding-padding {{ padding: 11px 10px 10px !important; }} #u_content_heading_76 .v-font-size {{ font-size: 10px !important; }} #u_content_heading_78 .v-container-padding-padding {{ padding: 23px 10px 19px !important; }} #u_content_heading_78 .v-font-size {{ font-size: 15px !important; }} #u_content_heading_78 .v-line-height {{ line-height: 100% !important; }} #u_content_text_31 .v-line-height {{ line-height: 100% !important; }} }}
				    </style>
				  
				  

				<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css?family=Montserrat:400,700&display=swap" rel="stylesheet" type="text/css"><!--<![endif]-->

				</head>

				<body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #e7e7e7;color: #000000">
				  <!--[if IE]><div class="ie-container"><![endif]-->
				  <!--[if mso]><div class="mso-container"><![endif]-->
				  <table style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #e7e7e7;width:100%" cellpadding="0" cellspacing="0">
				  <tbody>
				  <tr style="vertical-align: top">
				    <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
				    <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td align="center" style="background-color: #e7e7e7;"><![endif]-->
				    

				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 18px 0px 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 18px 0px 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:1px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/PURCHASE ORDER.png" alt="" title="" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 598px;" width="598" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_16" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: #ffffff;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="200" class="v-col-background-color" style="background-color: #ffffff;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_4" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:32px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/company.png" alt="Barcode " title="Barcode " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 23%;max-width: 43.7px;" width="43.7" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_87" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Company
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_2" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:11px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <p><strong>{}</strong></p>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="210" class="v-col-background-color" style="background-color: #ffffff;width: 210px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-35" style="max-width: 320px;min-width: 210px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_5" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:36px 5px 6px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/department.png" alt="Calendar " title="Calendar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 20%;max-width: 40px;" width="40" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_88" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Department
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_3" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <strong>{}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="190" class="v-col-background-color" style="background-color: #ffffff;width: 190px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-31p67" style="max-width: 320px;min-width: 190px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_6" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:31px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/currency.png" alt="Dollar " title="Dollar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 24%;max-width: 43.2px;" width="43.2" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_89" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Total
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_4" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:12px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <strong>₹ {}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_52" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #ffffff;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: #ffffff;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				    <tbody>
				      <tr style="vertical-align: top">
				        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				          <span>&#160;</span>
				        </td>
				      </tr>
				    </tbody>
				  </table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_36" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="200" class="v-col-background-color" style="background-color: #ffffff;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_12" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:34px 5px 0px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/po_number.png" alt="Barcode " title="Barcode " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 23%;max-width: 43.7px;" width="43.7" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_90" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Number
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:12px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <strong>{}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="210" class="v-col-background-color" style="background-color: #ffffff;width: 210px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-35" style="max-width: 320px;min-width: 210px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_13" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 5px 5px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/user.png" alt="Calendar " title="Calendar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 17%;max-width: 34px;" width="34" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_91" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Supplier
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_35" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <strong>{}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="190" class="v-col-background-color" style="background-color: #ffffff;width: 190px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-31p67" style="max-width: 320px;min-width: 190px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_image_14" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 5px 1px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				<table width="100%" cellpadding="0" cellspacing="0" border="0">
				  <tr>
				    <td class="v-text-align" style="padding-right: 0px;padding-left: 0px;" align="center">
				      
				      <img align="center" border="0" src="https://hkmjerp.in/files/status.png" alt="Dollar " title="Dollar " style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 20%;max-width: 36px;" width="36" class="v-src-width v-src-max-width"/>
				      
				    </td>
				  </tr>
				</table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_92" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 16px;">
				    Status
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				<table id="u_content_heading_36" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:12px 10px 38px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    <strong>{}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div id="u_column_121" class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				    <tbody>
				      <tr style="vertical-align: top">
				        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				          <span>&#160;</span>
				        </td>
				      </tr>
				    </tbody>
				  </table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="269" class="v-col-background-color" style="background-color: #1b1c4a;width: 269px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-44p84" style="max-width: 320px;min-width: 269px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_67" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Item</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="112" class="v-col-background-color" style="background-color: #1b1c4a;width: 112px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-18p66" style="max-width: 320px;min-width: 112px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_68" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Qty</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="99" class="v-col-background-color" style="background-color: #1b1c4a;width: 99px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-16p5" style="max-width: 320px;min-width: 99px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_69" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Rate</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="120" class="v-col-background-color" style="background-color: #1b1c4a;width: 120px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-20" style="max-width: 320px;min-width: 120px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_70" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Price</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				{}


				<div id="u_row_37" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 1px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 1px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="194" class="v-col-background-color" style="background-color: #ffffff;width: 194px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-32p39" style="max-width: 320px;min-width: 194px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_37" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 20px;">
				    <strong>GST / Extra</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="406" class="v-col-background-color" style="background-color: #1b1c4a;width: 406px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-67p61" style="max-width: 320px;min-width: 406px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_66" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>₹ {}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_35" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #fafafa;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: #fafafa;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="194" class="v-col-background-color" style="background-color: #ffffff;width: 194px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-32p29" style="max-width: 320px;min-width: 194px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_31" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 20px;">
				    <strong>TOTAL</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="406" class="v-col-background-color" style="background-color: #1b1c4a;width: 406px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-67p71" style="max-width: 320px;min-width: 406px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_15" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>₹ {}</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #fdfdfd;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #fdfdfd;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				    <tbody>
				      <tr style="vertical-align: top">
				        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
				          <span>&#160;</span>
				        </td>
				      </tr>
				    </tbody>
				  </table>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_25" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:40px 10px 0px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 100%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Extra Description</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <div class="v-text-align v-line-height" style="line-height: 140%; text-align: left; word-wrap: break-word;">
				    <p style="font-size: 14px; line-height: 140%; text-align: center;"><span style="font-family: Montserrat, sans-serif; font-size: 14px; line-height: 14px;">{}</span></p>
				  </div>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #caf8f8;width: 600px;padding: 12px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #caf8f8;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 12px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_105" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 22px;">
				    <strong>Applicable ALM</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_19" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="200" class="v-col-background-color" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_5" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Recommender</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="200" class="v-col-background-color" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_6" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>First Approval</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="200" class="v-col-background-color" style="background-color: #1b1c4a;width: 200px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p33" style="max-width: 320px;min-width: 200px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_7" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 18px;">
				    <strong>Final Approver</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div id="u_row_24" class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="201" class="v-col-background-color" style="background-color: #f6f6f6;width: 201px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p56" style="max-width: 320px;min-width: 201px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_22" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    {}
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="201" class="v-col-background-color" style="background-color: #f6f6f6;width: 201px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-33p56" style="max-width: 320px;min-width: 201px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_77" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    {}
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				<!--[if (mso)|(IE)]><td align="center" width="197" class="v-col-background-color" style="background-color: #f6f6f6;width: 197px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-32p88" style="max-width: 320px;min-width: 197px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_76" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
				    {}
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>



				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #ffffff;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #ffffff;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_heading_78" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:38px 10px 25px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; color: #1b1c4a; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 24px;">
				    <strong>Applicable Actions</strong>
				  </h1>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>


				<div style="background-color:#ffffff;margin:20px 0px;" height=10>
				
				<table cellspacing="0" cellpadding="0">
				    <tbody>
				        <tr>
				            <td bgcolor="#349106">
				                <a href="{}" target="_blank" style="color:#fff; border:4px solid #000; border-radius:2px; display:inline-block; font-family:Montserrat, sans-serif; font-size:14px; font-weight:bold; padding:8px 12px; text-decoration:none">Approve </a>
				            </td>
				            <td style="width:20px" width="20">
				            </td>
				            <td bgcolor="#cf3853">
				                <a href="{}" target="_blank" style="color:#fff; border:4px solid #000; border-radius:2px; display:inline-block; font-family:Montserrat, sans-serif; font-size:14px; font-weight:bold; padding:8px 12px; text-decoration:none">Reject</a>
				            </td>
				            <td style="width:20px" width="20">
				            </td>
				            <td bgcolor="#c7cc37">
				                <a href="{}" target="_blank" style="color:#000; border:4px solid #000; border-radius:2px; display:inline-block; font-family:Montserrat, sans-serif; font-size:14px; font-weight:bold; padding:8px 12px; text-decoration:none">View</a>
				            </td>

				        </tr>
				    </tbody>
				</table>

				</div>




				<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
				  <div class="u-row v-row-columns-background-color-background-color" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
				    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
				      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: transparent;"><![endif]-->
				      
				<!--[if (mso)|(IE)]><td align="center" width="600" class="v-col-background-color" style="background-color: #1b1c4a;width: 600px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
				<div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
				  <div class="v-col-background-color" style="background-color: #1b1c4a;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
				  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
				  
				<table id="u_content_text_31" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
				  <tbody>
				    <tr>
				      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:30px 10px 40px;font-family:arial,helvetica,sans-serif;" align="left">
				        
				  <div class="v-text-align v-line-height" style="color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word;">
				    <p style="font-size: 14px; line-height: 100%;"><span style="font-family: Montserrat, sans-serif; font-size: 10px; line-height: 10px;">Hare Krishna Hare Krishna Krishna Krishna Hare Hare</span></p>
				<p style="font-size: 14px; line-height: 100%;"><span style="font-family: Montserrat, sans-serif; font-size: 10px; line-height: 10px;">Hare Rama Hare Rama Rama Rama Hare Hare</span></p>
				  </div>

				      </td>
				    </tr>
				  </tbody>
				</table>

				  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
				  </div>
				</div>
				<!--[if (mso)|(IE)]></td><![endif]-->
				      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
				    </div>
				  </div>
				</div>


				    <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
				    </td>
				  </tr>
				  </tbody>
				  </table>
				  <!--[if mso]></div><![endif]-->
				  <!--[if IE]></div><![endif]-->
				</body>

				</html>

				
	""".format(
        doc.company,
        doc.department,
        doc.rounded_total,
        doc.name,
        doc.supplier_name,
        # frappe.db.get_value("User",{"email":doc.owner}, "full_name"),
        doc.workflow_state,
        item_str(doc),
        doc.base_total_taxes_and_charges,
        doc.rounded_total,
        doc.extra_description,
        doc.recommended_by,
        doc.first_approving_authority,
        doc.final_approving_authority,
        approval_link,
        rejection_link,
        frappe.utils.get_url_to_form(doc.doctype, doc.name),
    )
    return message


def item_str(doc):
    item_string = ""
    for idx, item in enumerate(doc.items):
        item_string = (
            item_string
            + """								
									<div class="u-row-container v-row-padding--vertical v-row-background-color" style="padding: 0px;background-color: transparent">
									  <div class="u-row v-row-columns-background-color-background-color no-stack" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: #f6f6f6;">
									    <div style="border-collapse: collapse;display: table;width: 100%;background-color: transparent;">
									      <!--[if (mso)|(IE)]><table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td class="v-row-background-color" style="padding: 0px;background-color: transparent;" align="center"><table cellpadding="0" cellspacing="0" border="0" style="width:600px;"><tr class="v-row-columns-background-color-background-color" style="background-color: #f6f6f6;"><![endif]-->
									      
									<!--[if (mso)|(IE)]><td align="center" width="271" class="v-col-background-color" style="background-color: #f6f6f6;width: 271px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
									<div class="u-col u-col-45p17" style="max-width: 320px;min-width: 271px;display: table-cell;vertical-align: top;">
									  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
									  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
									  
									<table id="u_content_heading_72" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
									  <tbody>
									    <tr>
									      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:arial,helvetica,sans-serif;" align="left">
									        
									  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: left; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
									    {}
									  </h1>

									      </td>
									    </tr>
									  </tbody>
									</table>

									  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
									  </div>
									</div>
									<!--[if (mso)|(IE)]></td><![endif]-->
									<!--[if (mso)|(IE)]><td align="center" width="112" class="v-col-background-color" style="background-color: #f6f6f6;width: 112px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
									<div class="u-col u-col-18p66" style="max-width: 320px;min-width: 112px;display: table-cell;vertical-align: top;">
									  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
									  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
									  
									<table id="u_content_heading_73" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
									  <tbody>
									    <tr>
									      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
									        
									  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
									    <strong>{}</strong>
									  </h1>

									      </td>
									    </tr>
									  </tbody>
									</table>

									  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
									  </div>
									</div>
									<!--[if (mso)|(IE)]></td><![endif]-->
									<!--[if (mso)|(IE)]><td align="center" width="100" class="v-col-background-color" style="background-color: #f6f6f6;width: 100px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
									<div class="u-col u-col-16p67" style="max-width: 320px;min-width: 100px;display: table-cell;vertical-align: top;">
									  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
									  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
									  
									<table id="u_content_heading_74" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
									  <tbody>
									    <tr>
									      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
									        
									  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
									    <strong>₹ {}</strong>
									  </h1>

									      </td>
									    </tr>
									  </tbody>
									</table>

									  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
									  </div>
									</div>
									<!--[if (mso)|(IE)]></td><![endif]-->
									<!--[if (mso)|(IE)]><td align="center" width="117" class="v-col-background-color" style="background-color: #f6f6f6;width: 117px;padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;" valign="top"><![endif]-->
									<div class="u-col u-col-19p5" style="max-width: 320px;min-width: 117px;display: table-cell;vertical-align: top;">
									  <div class="v-col-background-color" style="background-color: #f6f6f6;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
									  <!--[if (!mso)&(!IE)]><!--><div style="padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;"><!--<![endif]-->
									  
									<table id="u_content_heading_75" style="font-family:arial,helvetica,sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
									  <tbody>
									    <tr>
									      <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:20px 10px;font-family:arial,helvetica,sans-serif;" align="left">
									        
									  <h1 class="v-text-align v-line-height v-font-size" style="margin: 0px; line-height: 140%; text-align: center; word-wrap: break-word; font-weight: normal; font-family: 'Montserrat',sans-serif; font-size: 14px;">
									    <strong>₹ {}</strong>
									  </h1>

									      </td>
									    </tr>
									  </tbody>
									</table>

									  <!--[if (!mso)&(!IE)]><!--></div><!--<![endif]-->
									  </div>
									</div>
									<!--[if (mso)|(IE)]></td><![endif]-->
									      <!--[if (mso)|(IE)]></tr></table></td></tr></table><![endif]-->
									    </div>
									  </div>
									</div>     
								  """.format(
                item.item_name,
                str(item.qty) + " " + item.uom,
                item.net_rate,
                item.net_amount,
            )
        )

    return item_string
