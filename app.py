from flask import Flask, request, jsonify
import dns.resolver

app = Flask(__name__)

def usa_intune(dominio):
    try:
        cname_targets = []
        for sub in ['enterpriseenrollment', 'enterpriseregistration']:
            fqdn = f"{sub}.{dominio}"
            try:
                answers = dns.resolver.resolve(fqdn, 'CNAME')
                for rdata in answers:
                    cname_targets.append(str(rdata.target))
            except:
                continue
        for cname in cname_targets:
            if "manage.microsoft.com" in cname:
                return True

        try:
            txt_records = dns.resolver.resolve(dominio, 'TXT')
            for record in txt_records:
                if any("MS=" in txt.decode() for txt in record.strings):
                    return True
        except:
            pass
    except:
        pass
    return False

@app.route("/check_intune", methods=["GET"])
def check_intune():
    dominio = request.args.get("dominio")
    if not dominio:
        return jsonify({"usa_intune": "Error: dominio faltante"})
    resultado = usa_intune(dominio)
    return jsonify({"usa_intune": "Sí" if resultado else "No"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
