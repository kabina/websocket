def cert():
    import OpenSSL.crypto
    import datetime

    # CA 인증서 로딩
    ca_cert_file = "devevspcharger-rootca.crt"  # CA 인증서 파일 경로
    with open(ca_cert_file, 'rb') as ca_cert_file:
        ca_cert_data = ca_cert_file.read()
        ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, ca_cert_data)

    # 현재 시간 확인
    now = datetime.datetime.now()
    from datetime import datetime
    notBefore = datetime.strptime(str(ca_cert.get_notBefore(), 'utf-8'), '%Y%m%d%H%M%SZ')
    notAfter = datetime.strptime(str(ca_cert.get_notAfter(), 'utf-8'), '%Y%m%d%H%M%SZ')


    # CA 인증서 유효성 체크
    if now < notBefore:
        print("CA 인증서가 아직 유효하지 않습니다.")
    elif now > notAfter:
        print("CA 인증서가 만료되었습니다.")
    else:
        print("CA 인증서가 유효합니다.")

    # 검증할 인증서 로딩
    cert_file = "devevspcharger.uplus.co.kr.crt"  # 검증할 인증서 파일 경로
    with open(cert_file, 'rb') as cert_file:
        cert_data = cert_file.read()
        cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)

    # 검증 설정
    store = OpenSSL.crypto.X509Store()
    store.add_cert(ca_cert)
    store_ctx = OpenSSL.crypto.X509StoreContext(store, cert)

    # 인증서 검증
    try:
        store_ctx.verify_certificate()
        print("인증서가 CA에 의해 검증되었습니다.")
        if cert.has_expired():
            print("인증서가 만료되었습니다.")
        elif now > notAfter:
            print("인증서가 만료되었습니다.")
        else:
            print("인증서가 유효합니다.")
    except OpenSSL.crypto.X509StoreContextError as e:
        print("인증서 검증에 실패하였습니다: {}".format(e))
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cert()

