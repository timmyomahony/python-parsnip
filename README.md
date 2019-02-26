**WARNING** This code is no longer maintained and is unlikely to work due to updates on the mobile proviers webtexting applications

---

![Screenshot](https://github.com/timmyomahony/python-parsnip/raw/master/parsnip-screen-small.jpg)

`Parsnip` is a basic python interface to allow the sending of web texts via the main 4 Irish mobile operators websites. It is influenced by [cabbage](http://cabbagetexter.com/), a popular `php` implementation. 

* **Meteor** : [http://mymeteor.ie](https://www.mymeteor.ie/mymeteorapi/index.cfm)
* **O2** :  [http://o2online.ie](https://messaging.o2online.ie/smscenter_send.osp)
* **Vodafone** : [http://vodafone.ie](https://www.vodafone.ie/myv/messaging/webtext/Process.shtml)
* **Three** : [http://three.ie](http://webtext.three.ie/send.jsp)

## Install

Either `pip install python-parsnip` or get the latest code via GitHub with `pip install -e git+https://github.com/timmyomahony/python-parsnip.git#egg=python-parsnip`
	
## Usage

	import parsnip
	texter = parsnip.get_webtexter("Meteor", "0851111111", "1234")
	texter.login()
	texter.send("Heyo", ["0866666666", "0877777777", "0863333333"])
	print texter.get_remaining_webtexts()
	255
    texter.logout()
	
* `get_webtexter(operator, phone_number, online_pin)` : is a factory method which returns an instance of `Webtexter`. 
* A webtexter instance has the following methods:
  * `login()` : login to remote operator site
  * `logout()` : clear cookies and perform logout on remote operator site
  * `send(message, recipients)` : sends a web text to the provided recipients, where `recipient` is either a comma separated string of phone numbers, or a list of phone numbers. 
  * `get_remaining_webtexts` : returns an integer 

## Features

* __Chunking:__ For messages that have more characters then the provider allows (i.e. sending a message greater than 160 characters on Three), the message will be broken into smaller chunks and sent separately. The same can be said for recipients : if there are more recipients then the provider handles, they are split up and the message numerous times
