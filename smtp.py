def send_mail(msg):
    if(type(msg) == dict):
        from smtplib import SMTP
        from json import loads

        with open('smtp.json','r') as file:
            config = loads(file.read())
            fixed_msg = ""
            for x in msg:
                fixed_msg += f"\n{x} -> {msg[x][0]} zl\n{msg[x][1]}"
                fullmsg = f'Subject: Cena spadla !!!\n{fixed_msg}'
                # print(fullmsg)

        with SMTP(config["smtp_server"],config["port"]) as server:
            server.starttls()
            server.login(config["email"],config["password"])
            print("Login success")
            server.sendmail(config["email"],"xxkubanxx@gmail.com",fullmsg)
            print("Mail sent")
    else:
        print("Arg must be dict type")
