# OLXLookUp
Lookup OLX Listings in fixed time intervals and send whatsapp notifications using Twilio Whatsapp API.

Built using Python, BeautifulSoup and Twilio.

To setup tracking for your own filters:

1. Fork the Repository.
2. Setup your Twilio Account.
3. Setup the following Environment Variables under Settings/Secrets
  - CONTACT_NUMBER (Phone Number to which you need to receive the Whatsapp Notifications)
  - OLX_URL (OLX URL with all your filters)
  - TWILIO_ACCOUNT_SID
  - TWILIO_AUTH_TOKEN
4. Setup github actions with the existing workflow

### Collaboration

Feel free to create issues or raise PRs for additional features
  
