### Parsnip ###

`Parsnip` is a basic python interface to allow the sending of web texts via the main 4 Irish mobile operators websites. It is influenced by [cabbage](http://cabbagetexter.com/), a popular `php` implementation. 

* **Meteor** : [http://mymeteor.ie](https://www.mymeteor.ie/mymeteorapi/index.cfm)
* **O2** :  [http://o2online.ie](https://messaging.o2online.ie/smscenter_send.osp)
* **Vodafone** : [http://vodafone.ie](https://www.vodafone.ie/myv/messaging/webtext/Process.shtml)
* **Three** : [http://three.ie](http://webtext.three.ie/send.jsp)

###Usage###

	import parsnip
	texter = parsnip.get_webtexter("Meteor", "0851111111", "1234")
	texter.login()
	texter.send("Heyo", ["0866666666", ["0877777777", "0863333333"])
	print texter.get_remaining_webtexts()
	255
	

###Features###

* For messages that have more characters then the provider allows (i.e. sending a message greater than 160 characters on Three), the message will be broken into smaller chunks and sent separately. The same can be said for recipients : if there are more recipients then the provider handles, they are split up and the message numerous times

###TODO###

* incorporate group texting
* add ellipses to chunked messages

###Contact###
timmy@pastylegs.com