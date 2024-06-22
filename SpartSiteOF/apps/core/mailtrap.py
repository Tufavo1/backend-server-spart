import mailtrap as mt

mail = mt.Mail(
    sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
    to=[mt.Address(email="saganspartan@gmail.com")],
    subject="You are awesome!",
    text="Congrats for sending test email with Mailtrap!",
    category="Integration Test",
)

client = mt.MailtrapClient(token="d1dfc46817d678d13d6ea655d1bbb914")
client.send(mail)
