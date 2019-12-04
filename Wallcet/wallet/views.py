from django.shortcuts import render
from web3 import Web3
from django.http import HttpResponse
from .models import Cuenta, Wallet
from .forms import nuevaWalletForm
from passlib.hash import pbkdf2_sha256

from django.core.mail import send_mail
from django.conf import settings

def index(request):

    # connection to a local blockchain
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))


    if request.method == 'POST':

        # creating a new account
        if 'modalCrear' in request.POST:

            # creacion de wallet con pasword encriptado
            contra = request.POST['kontra']
            contrasenia_encryptada = pbkdf2_sha256.encrypt(contra, rounds=12000, salt_size = 32)
            wallet_instance = Wallet.objects.create(eMail= request.POST['imail'], contrasenia = contrasenia_encryptada)
            dir = request.POST['imail']

            # creacion de la cuenta asociada
            aletoriedad = request.POST['randomness']
            acct = web3.eth.account.create(aletoriedad)
            acc_addr = acct.address
            acc_priv_k = acct.privateKey.hex()
            balan = web3.eth.getBalance(acc_addr)
            cuenta_instance = Cuenta.objects.create(walle=wallet_instance, llavePrivada=acc_priv_k, llavePublica=acc_addr, balance=balan )

            # saving all accounts into a an array
            accounts_all = web3.eth.accounts



            context ={'account_list': accounts_all,'priv_account': acc_priv_k,'addr_account': acc_addr, 'balance': balan,'e_mail': dir,'contrasenia':contra,}
            return render(request, 'wallet/nuevaWallet.html', context)


        if 'modalAbrir' in request.POST:
            pwd = request.POST['pwd_acc']
            dir = request.POST['dir_acc_opn']
            bal = web3.fromWei(web3.eth.getBalance(dir),"ether")
            accounts_all = web3.eth.accounts


            context ={'account_list': accounts_all,'priv_account': pwd,'addr_account': dir, 'balance': bal,}
            return render(request, 'wallet/index.html', context)


    # log into an existing account with address and private key

    accounts_all = web3.eth.accounts
    context = {'account_list': accounts_all,}
    return render(request, 'wallet/index.html', context)

def home(request):

    # connection to a local blockchain
    ganache_url = "http://127.0.0.1:7545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    if request.method == 'POST':
        if 'modalEnviar' in request.POST:
                # needed variables for rawTransaction
            src_acc = request.POST['cuenta_fuente']
            prv_key = request.POST['llave_privada']
            des_acc = request.POST['cuenta_destino']
            amount = request.POST['cantidad_eth']
                # get the nonce
            nonce = web3.eth.getTransactionCount(src_acc)
                # build a transaction
            tx = {
                'nonce': nonce,
                'to': des_acc,
                'value': web3.toWei(amount, 'ether'),
                'gas': 2000000,
                'gasPrice': web3.toWei('50', 'gwei')
            }
                # sign transaction
            signed_tx = web3.eth.account.signTransaction(tx, prv_key)
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(web3.toHex(tx_hash))
            dir = request.POST['emai']
            wallet_ins = Wallet.objects.get(eMail=request.POST['emai'])
            accounts_all = Cuenta.objects.all().filter(walle_id= wallet_ins.id)

            # encontrando todos los balances
            balance_list = []
            i=0
            for x in accounts_all:
                balance_list.append(x)
                balance_list[i].balance = web3.fromWei(web3.eth.getBalance(x.llavePublica),"ether")
                i+=1

            context ={'account_list': accounts_all, 'e_mail': dir}
            return render(request, 'wallet/home.html', context)

        if 'modalCrearCuen' in request.POST:
            aletoriedad = request.POST['randomness']
            dir = request.POST['emai']
            acct = web3.eth.account.create(aletoriedad)
            acc_addr = acct.address
            acc_priv_k = acct.privateKey.hex()
            balan = web3.eth.getBalance(acc_addr)
            wallet_ins = Wallet.objects.get(eMail=request.POST['emai'])
            cuenta_instance = Cuenta.objects.create(walle=wallet_ins, llavePrivada=acc_priv_k, llavePublica=acc_addr, balance=balan )
            accounts_all = Cuenta.objects.all().filter(walle_id= wallet_ins.id)

            # encontrando todos los balances
            balance_list = []
            i=0
            for x in accounts_all:
                balance_list.append(x)
                balance_list[i].balance = web3.fromWei(web3.eth.getBalance(x.llavePublica),"ether")
                i+=1


            context ={'account_list': accounts_all, 'e_mail': dir}
            return render(request, 'wallet/home.html', context)


        if 'bSiguiente' in request.POST:

            dir = request.POST['emai']
            wallet_ins = Wallet.objects.get(eMail=request.POST['emai'])
            accounts_all = Cuenta.objects.all().filter(walle_id= wallet_ins.id)

            # encontrando todos los balances
            balance_list = []
            i=0
            for x in accounts_all:
                balance_list.append(x)
                balance_list[i].balance = web3.fromWei(web3.eth.getBalance(x.llavePublica),"ether")
                i+=1


            context ={'account_list': accounts_all, 'e_mail': dir}
            return render(request, 'wallet/home.html', context)


    pwd = request.POST['pwd_acc']
    dir = request.POST['dir_acc_opn']
    cuen = Wallet.objects.all().filter(eMail=dir)
    enc_pwd = cuen.values_list('contrasenia', flat=True)

    if cuen:
        validation = pbkdf2_sha256.verify(pwd, enc_pwd[0])
        if validation:
            wallet = Wallet.objects.get(eMail=dir)
            accounts_all = Cuenta.objects.all().filter(walle_id= wallet.id)

            # encontrando todos los balances
            balance_list = []
            i=0
            for x in accounts_all:
                balance_list.append(x)
                balance_list[i].balance = web3.fromWei(web3.eth.getBalance(x.llavePublica),"ether")
                i+=1

            # enviar mensaje al correo electronico registrado
            subject = 'Acabas de abrir tu monedero?'
            message = 'Tu monedero acaba de ser abierto por un dispositivo. Si tu no has ocupado el monedero puede significar que alguien conoce tus credenciales.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [dir,]
            send_mail(subject, message, email_from, recipient_list)

            context ={'account_list': accounts_all, 'e_mail': dir,}
            return render(request, 'wallet/home.html', context)


    context ={'account_list': accounts_all,'priv_account': pwd,'addr_account': dir, 'balance': bal,}
    return render(request, 'wallet/home.html', context)
