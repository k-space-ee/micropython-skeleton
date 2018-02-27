# Connect to wireless network as client
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("itcollege")
