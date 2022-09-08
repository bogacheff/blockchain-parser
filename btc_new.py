from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests as req
import os
import colorama
from colorama import Fore, Back, Style
colorama.init()

chromedriver = "/usr/local/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

os.system('cls' if os.name == 'nt' else 'clear')
print ("*************** PARSE START ******************")

max_block = input("Enter max value for block: ")
max_block = int(max_block)
#max_block = 12665
sleep = input("Enter sleep ms: ")
sleep = float(sleep)

user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')

def get_html(page):
	resp = req.get("https://www.blockchain.com/btc/blocks?page=" + str(page))
	print (Fore.RED + "################### PARSE PAGE: [" + str(page) + "] ###################")
	print(Style.RESET_ALL)
	soup = BeautifulSoup(resp.text, 'lxml')
	return (soup)

def get_balance(wallet):
	url = "https://privatekeys.pw/quick-search?query=" + str(wallet)
	print (Fore.RED + "WALLET PARSE: " + str(wallet))
	print("URL WALLET" + url)
	print(Style.RESET_ALL)
	driver.get(url)
	time.sleep(sleep)
	soup = BeautifulSoup(driver.page_source, "html.parser")
	#driver.quit()
	return (soup)

coin_array = []

while int(max_block) >= 1:
	soup = get_html(max_block)
	res = soup.findAll("div", width="40%")
	for i in res:
		parent = i.findAll("a")
		for z in parent:
			b = z.attrs["href"]
			coin_array.append(b.split('/')[3])

	for x in coin_array:
		#print(x)
		wallet = get_balance(x)
		#span_js = wallet.findAll("span", {"class": "js-balances-bitcoin"})
		total_balance = wallet.find("span", {"data-original-title" : "Total balance"}).getText()
		total_received = wallet.find("span", {"data-original-title" : "Total received"}).getText()
		total_txcount = wallet.find("span", {"data-original-title" : "Total TX count"}).getText()

		print("Total balance:" + total_balance)
		print("Total received:" + total_received)
		print("Total TX count:" + total_txcount)

		if float(total_received) > 0:
			print('Total received > 0 SEND TO TELEGRAM')

		coin_array = []

	max_block = max_block - 1


