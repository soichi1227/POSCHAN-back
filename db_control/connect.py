import platform
from sqlalchemy import create_engine
import os
import tempfile
import atexit
from dotenv import load_dotenv

load_dotenv()
print("Current Directory:", os.getcwd())
DATABASE_URL ="mysql+pymysql://Tech0Gen8TA3:gen8-1-ta%403@tech0-gen-8-step4-db-3.mysql.database.azure.com:3306/pos_chomu"

# os.getenv("DB_URL")
pem_content ="-----BEGIN CERTIFICATE-----\\nMIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\\nMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\\nd3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\\nQTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\\nMRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\\nb20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\\n9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\\nCSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\\nnh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\\n43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\\nT19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\\ngdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\\nBgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\\nTLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\\nDQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\\nhMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\\n06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\\nPnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\\nYSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\\nCAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\\n-----END CERTIFICATE-----"

# os.getenv("SSL_CA_STR")

print(DATABASE_URL)
print(pem_content)

# SSL証明書内容の確認と処理
if pem_content is None:
    raise ValueError("SSL_CA_CERT is not set in environment variables.")

pem_content = pem_content.replace("\\n", "\n").replace("\\", "")

# 一時ファイル作成
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".pem") as temp_pem:
    temp_pem.write(pem_content)
    temp_pem_path = temp_pem.name

with open(temp_pem_path, "r") as temp_pem:
    print("=====Temporary certificate file content:=====")
    print(temp_pem_path)
    # print(temp_pem.read())

# データベース接続設定
engine = create_engine(
    DATABASE_URL, # type: ignore
    connect_args={
        "ssl": {
            "ca": temp_pem_path
        }
    }
)

# 一時ファイル削除の登録
def cleanup_temp_file(path):
    if os.path.exists(path):
        os.remove(path)

# Python正常終了時に一時ファイルを削除
atexit.register(cleanup_temp_file, temp_pem_path)