query1="select * from cus"
style1="-----------------------------------------------\n"
global MeniuOptionName, MeniuOption, Quantity, sl, cur, c, named, addd, t, vc_id, B

def select_option_from_meniu(e):
    p = p.curselection()
    x = 0
    sl1 = ''
    from datetime import date
    now = time.localtime()
    cur.execute("select * from med")
    for i in cur:
        if x == int(p[0]):
            sl1 = int(i[0])
            break
        x += 1
    c.commit()
    print(sl1)
    MeniuOptionName = n[x]
    print(MeniuOptionName)

def append_to_bill():
    sl.append(sl1)
    MeniuOption.append(MeniuOptionName)
    Quantity.append(qtys.get())
    print(Quantity)
    print(sl[len(sl) - 1], MeniuOption[len(MeniuOption) - 1], Quantity[len(Quantity) - 1])

def get_customer_info():
    
    cur.execute(query1)
    for i in cur:
        if vc_id.get() != '' and int(vc_id.get()) == i[2]:
            named = i[0]
            addd = i[1]
            Label(st, text=named, width=20).grid(row=1, column=1)
            Label(st, text=addd, width=20).grid(row=2, column=1)
            Label(st, text=i[2], width=20).grid(row=3, column=1)
            Label(st, text='Valued Customer!').grid(row=4, column=1)
            t = 1
            break
    c.commit()

def create_bill():
    price = [0.0] * 10
    det = ['', '', '', '', '', '', '', '']
    det[2] = str(sl)
    for i in range(len(sl)):
        print(sl[i], ' ', Quantity[i], ' ', MeniuOption[i])
    for j in range(len(sl)):
        cur.execute("select * from med where sl_no=?", (sl[j],))
        for i in cur:
            price[j] = int(Quantity[j]) * float(i[4])
            print(Quantity[j], price[j])
            cur.execute("update med set QuantityLeft=? where sl_no=?", (int(i[3]) - int(Quantity[j]), sl[j]))
        c.commit()
    det[5] = str(random.randint(100, 999))
    B = 'bill_' + str(det[5]) + '.txt'
    total = 0.00
    for i in range(10):
        if price[i] != '':
            total += price[i]  # totalling
    m = '\n\n\n'
    m += "===============================================\n"
    m += "                                  No :%s\n\n" % det[5]
    m += " EVANZ MEDICAL STORE COMPANY\n"
    m += " BINALBAGAN BRANCH, NEGROS OCCIDENTAL\n\n"
    m += style1
    if t == 1:
        m += "Name: %s\n" % named
        m += "Address: %s\n" % addd
        det[0] = named
        det[1] = addd
        cur.execute('select * from cus')
        for i in cur:
            if i[0] == named:
                det[7] = i[2]
    else:
        m += "Name: %s\n" % name1.get()
        m += "Address: %s\n" % add.get()
        det[0] = name1.get()
        det[1] = add.get()
    m += style1
    m += "Product                      Quantity.       Price\n"
    m += style1
    for i in range(len(sl)):
        if MeniuOption[i] != 'nil':
            s1 = ' '
            s1 = (MeniuOption[i]) + (s1 * (27 - len(MeniuOption[i]))) + s1 * (3 - len(Quantity[i])) + Quantity[i] + s1 * (
                        15 - len(str(price[i]))) + str(price[i]) + '\n'
            m += s1
    m += style1
    if t == 1:
        ntotal = total * 0.8
        m += 'Total' + (' ' * 25) + (' ' * (15 - len(str(total)))) + str(total) + '\n'
        m += "Valued customer Discount" + (' ' * (20 - len(str(total - ntotal)))) + '-' + str(total - ntotal) + '\n'
        m += "-----------------------------------------------\n"
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(ntotal)))) + 'PHP ' + str(ntotal) + '\n'
        det[3] = str(ntotal)
    else:
        m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(total)))) + 'PHP ' + str(total) + '\n'
        det[3] = str(total)
    m += "-----------------------------------------------\n\n"
    m += "Dealer 's signature:___________________________\n"
    m += "===============================================\n"
    print(m)
    p = time.localtime()
    det[4] = str(p[2]) + '/' + str(p[1]) + '/' + str(p[0])
    det[6] = m
    bill = open(B, 'w')
    bill.write(m)
    bill.close()
    cur.execute('insert into bills values(?,?,?,?,?,?,?,?)',
                (det[0], det[1], det[2], det[3], det[4], det[5], det[6], det[7]))
    c.commit()
