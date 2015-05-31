import mechanicalsoup
import datetime
import arrow
from models import Tracking

browser = mechanicalsoup.Browser()

login_page = browser.get('http://183.177.124.6/24online/webpages/myaccountlogin.jsp')

login_form = login_page.soup.select('form')[0]

login_form.select('[name="username"]')[0]['value'] = ''
login_form.select('[name="password"]')[0]['value'] = ''

page2 = browser.submit(login_form, login_page.url)

remaining_data = page2.soup.select('#datausagediv1 > table > tr > td > font')[-1].text

package_expiry = page2.soup.select('td.inputtd > font')
package_expiry_date = datetime.datetime.strptime(package_expiry[5].text, '%d/%m/%Y %H:%M')
remaining_data

add_data = Tracking.create(remaining_data=remaining_data.strip('MBmbKGkg'))
add_data.save()

expires_in = package_expiry_date - datetime.datetime.now()
print "Expires in {} days".format(expires_in.days)
data_in_gb = round(float(remaining_data.strip('GMKBgmkb'))/1024, 2)
print "{}, or {} GB of data remaining".format(remaining_data, data_in_gb)

today = datetime.date.today()

last_30_days = arrow.now().replace(days=-30).naive


query = Tracking.select().where(Tracking.added_time >= last_30_days).order_by(Tracking.added_time.asc())

first_day = list(query)[0]
last_day = list(query)[-1]

print "Used {} MB of data in the last 30 days, as recorded in DB.".format(first_day.remaining_data - last_day.remaining_data)
print "Used on average {} MB of data per day in last 30 days.".format((first_day.remaining_data - last_day.remaining_data)/30)