from flask import Flask, request, jsonify
import dns.resolver

app = Flask(__name__)

def usa_intune(dominio):
    intune_dns = []
    otras_dns = []
    try:
        cname_targets = []
        for sub in ['enterpriseenrollment', 'enterpriseregistration']:
            fqdn = f"{sub}.{dominio}"
            try:
                answers = dns.resolver.resolve(fqdn, 'CNAME')
                for rdata in answers:
                    cname = str(rdata.target)
                    cname_targets.append(cname)
            except:
                continue

        # Clasificamos cada cname si es intune o no
        for cname in cname_targets:
            if "manage.microsoft.com" in cname:
                intune_dns.append(cname)
            else:
                otras_dns.append(cname)

        # Revisamos TXT records, los ponemos en "otras_dns" para ejemplo
        try:
            txt_records = dns.resolver.resolve(dominio, 'TXT')
            for record in txt_records:
                for txt in record.strings:
                    texto = txt.decode()
                if "MS=" in texto:
                    otras_dns.append(texto)
                else:
                    otras_dns.append(texto)
                except:
            pass

        usa_intune_flag = len(intune_dns) > 0

        return usa_intune_flag, intune_dns, otras_dns

    except Exception as e:
        return False, [], []

@app.route("/check_intune", methods=["GET"])
def check_intune():
    dominio = request.args.get("dominio")
    if not dominio:
        return jsonify({"error": "dominio faltante"})

    resultado, intune_dns, otras_dns = usa_intune(dominio)

    return jsonify({
        "intune_usage": "true" if resultado else "false",
        "intune_dns": intune_dns,
        "otras_dns": otras_dns
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
