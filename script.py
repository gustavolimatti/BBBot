from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from binascii import a2b_base64
import processing
from getpass import getpass

login = ""
password = ""

login = input("Abaixo precisaremos das suas credenciais do Globo.com.\nDigite seu email: ")
password = getpass()

loginUrl = "https://minhaconta.globo.com/"

url = input("Copie e cole a URL do site da votação: ")

browser = None
try:
	caps = DesiredCapabilities().CHROME.copy()
	caps["pageLoadStrategy"] = "eager"  #  interactive
	browser = webdriver.Chrome(capabilities=caps)
	# browser = webdriver.Chrome()
except:
	caps = DesiredCapabilities().FIREFOX.copy()
	caps["pageLoadStrategy"] = "eager"  #  interactive
	browser = webdriver.Firefox(capabilities=caps)
	# browser = webdriver.Firefox()

browser.set_window_position(0, 0)
browser.set_window_size(400, 768)
browser.get(loginUrl)

time.sleep(10)
print("\nfazendo o login...")
browser.find_element_by_id('login').send_keys(login)
browser.find_element_by_id('password').send_keys(password)
browser.find_elements_by_css_selector('#login-form .button')[0].click()

print("login finalizado...")

time.sleep(10)
browser.get(url)
time.sleep(5)

print("iniciando o bot")
while(1):
	try:
		# title = browser.find_elements_by_class_name('_1QJO-RxRXUUbq_pPU1oVZK')[0].text
		# title = browser.find_element_by_xpath('//*[@id="roulette-root"]/div/div[1]/div[3]/div/div/div')
		title = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[1]/div[3]/div/div/div').text
		
		break
	except:
		pass

#print("title: " + title)

titleParts = title.split('?')[1]
titleParts = titleParts.replace(' ou ', ', ')

#print(titleParts)

##### paredão triplo #####
namesHelp = titleParts.split(', ')
print(namesHelp)

names = []
for name in namesHelp:
	names.append(name.split(' ')[-1])
	
#print(names)

##### paredão duplo #####
#namesAux = titleParts.split(' ou ')
#names = [namesAux[0].strip(), namesAux[1]]

option = input("Quem você quer eliminar?\n1. "+names[0]+"\n2. "+names[1]+"\n3. "+names[2]+"\nDigite o número correspondente: ")
while not option in ["1", "2", "3"]:
	option = input("Quem você quer eliminar?\n1. "+names[0]+"\n2. "+names[1]+"\n3. "+names[2]+"\nDigite o número correspondente: ")

nameSearch = names[int(option)-1]
idxName = names.index(nameSearch)
totalVotes = 0

while True:
	element = []
	while(1):
		try:
			element = [
				browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[1]/div[4]/div[1]'),
				browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[1]/div[4]/div[2]'),
				browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[1]/div[4]/div[3]'),
			]
			break
		except:
			pass


	elementBtn = element[idxName]

	# scroll down
	browser.execute_script("window.scrollTo(0, 700)") 
  
	ac2 = ActionChains(browser)
	ac2.move_to_element(elementBtn).click().perform()
	time.sleep(3)

	outSideLoop = True
	innerLoop = True
	while outSideLoop:
		ac = ActionChains(browser)
		captchaBox = []

		vote_succeeded = False

		while innerLoop:
			try:
				captchaBox = browser.find_elements_by_class_name('gc__2Qtwp')
				if captchaBox != []:
					if len(captchaBox[0].text) > 2:
						break

				time.sleep(3)

				value = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[3]/div/div/div[1]/div[2]/button')
				if value.text != '':
					vote_succeeded = True
					outSideLoop = False
					innerLoop = False
					break
			except:
				pass

		if vote_succeeded:
			totalVotes += 1
			print(totalVotes, 'votos com sucesso')
			break
		
		imageSearchName = captchaBox[0].text.split('\n')[-1]
		print("procurando por " + imageSearchName)

		captcha = []
		while(1):
			try:
				captcha = browser.find_elements_by_class_name('gc__3_EfD')[0]
				break
			except:
				pass

		captchaSrc = captcha.get_attribute("src")

		data = captchaSrc.split(';base64,')[1]
		binary_data = a2b_base64(data)

		filename = imageSearchName + '.png'

		fd = open('BBB20/captchas/' + filename, 'wb')
		fd.write(binary_data)
		fd.close()

		processing.processImage(filename)
		points = processing.findInCaptcha(filename)
		
		if points != []:
			print("a imagem se encontra nos pontos: " + str(points[0]) + " X " + str(points[1]))
			print("o tamanho do captcha é " + str(captcha.size['width']) + " X " + str(captcha.size['height']))

			posX = points[0] - captcha.size['width']/2
			posY = points[1] - captcha.size['height']/2

			ac.move_to_element(captcha).move_by_offset(posX, posY).click().perform()
			time.sleep(3)
		else:
			print("erro - captcha não encontrado")
            
		time.sleep(3)
	
	browser.refresh()
	time.sleep(3)

