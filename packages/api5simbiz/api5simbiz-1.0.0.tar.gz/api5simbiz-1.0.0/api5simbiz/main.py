import requests

class fivesim:
   def __init__(self, api):
       self.api_key = api
       self.base_url = 'https://5sim.biz/v1/'
       self.headers = {'Authorization': f'Bearer {self.api_key}', 'Accept': 'application/json'}

   def get_profile(self):
        url = f'{self.base_url}user/profile'
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            resp = response.json()
            print(f'id: {resp["id"]}')
            print(f'Email: {resp["email"]}')
            print(f'Рейтинг: {resp["rating"]}')
            return (f'Баланс: {resp["balance"]}') # Сделал так потому что если везде поставить print() то выведет 4 строчки а 5 строчкой будет None
        else:
            raise Exception(response.status_code)

   def order_history(self, category, limit=None, offset=None, order=None, reverse=None):
       url = f'{self.base_url}user/orders'
       url_params = f'?category={category}'

       if limit is not None:
           url_params += f'&limit={limit}'
       if offset is not None:
           url_params += f'&offset={offset}'
       if order is not None:
           url_params += f'&order={order}'
       if reverse is not None:
           url_params += f'&reverse={reverse}'

       full_url = url + url_params
       response = requests.get(full_url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def payment_history(self, limit=None, offset=None, order=None, reverse=None):
       url = f'{self.base_url}user/payments'
       url_params = ''

       if limit is not None:
           url_params += f'?limit={limit}'
       if offset is not None:
           url_params += f'&offset={offset}'
       if order is not None:
           url_params += f'&order={order}'
       if reverse is not None:
           url_params += f'&reverse={reverse}'

       full_url = url + url_params
       response = requests.get(full_url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def max_prices(self):
       url = f'{self.base_url}user/max-prices'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def set_limit(self, product_name, price):
       url = f'{self.base_url}user/max-prices'
       data = {
           'product_name': product_name,
           'price': price
       }
       response = requests.post(url, headers=self.headers, data=data)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def delete_limit(self, product_name):
       url = f'{self.base_url}user/max-prices'
       data = {
           'product_name': product_name
       }
       response = requests.delete(url, headers=self.headers, data=data)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def product_request(self, country, operator):
       url = f'{self.base_url}guest/products/{country}/{operator}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def request_for_prices(self):
       url = f'{self.base_url}guest/prices'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def prices_by_country(self, country):
       url = f'{self.base_url}guest/prices?country={country}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def product_prices(self, product):
       url = f'{self.base_url}guest/prices?product={product}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def prices_by_country_and_product(self, country, product):
       url = f'{self.base_url}guest/prices?country={country}&product={product}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_number(self, country, operator, product, **kwargs):
       url = f'{self.base_url}user/buy/activation/{country}/{operator}/{product}'
       if kwargs:
           arguments = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
           full_url = f'{url}?{arguments}'
           response = requests.get(full_url, headers=self.headers)
           if response.status_code == 200:
               return response.text
           else:
               raise Exception(response.status_code)
       else:
           response = requests.get(url, headers=self.headers)
           if response.status_code == 200:
               return response.text
           else:
               raise Exception(response.status_code)

   def rent_phone(self, country, operator, product):
       url = f'{self.base_url}user/buy/hosting/{country}/{operator}/{product}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def rebuy_phone(self, number, product):
       url = f'{self.base_url}user/reuse/{product}/{number}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_sms(self, id):
       url = f'{self.base_url}user/check/{id}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def complete_order(self, id):
       url = f'{self.base_url}user/finish/{id}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def cancel_order(self, id):
       url = f'{self.base_url}user/cancel/{id}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def ban_phone(self, id):
       url = f'{self.base_url}user/ban/{id}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_sms_for_rent_number(self, id):
       url = f'{self.base_url}user/sms/inbox/{id}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_notifications(self, lang):
       url = f'{self.base_url}guest/flash/{lang}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def available_currency_reserves(self):
       url = f'{self.base_url}vendor/wallets'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def supplier_order_history(self, category):
       url = f'{self.base_url}vendor/orders?category={category}'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def supplier_payment_history(self):
       url = f'{self.base_url}vendor/payments'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def create_payment(self, receiver, method, amount, fee):
       url = f'{self.base_url}vendor/withdraw'
       data = {
           'receiver': receiver,
           'method': method,
           'amount': amount,
           'fee': fee
       }
       response = requests.post(url, headers=self.headers, data=data)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_countries(self):
       url = f'{self.base_url}guest/countries'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)

   def get_countries(self):
       url = f'{self.base_url}guest/countries'
       response = requests.get(url, headers=self.headers)
       if response.status_code == 200:
           return response.text
       else:
           raise Exception(response.status_code)