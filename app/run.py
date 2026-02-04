import uvicorn 
import ssl

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

ssl_context.load_cert_chain(
    certfile=r"app/certs/server/server.crt",
    keyfile=r"app/certs/server/server.key"
)

ssl_context.load_verify_locations(
    cafile = r"app/certs/ca/ca.crt"
    
)

ssl_context.verify_mode = ssl.CERT_REQUIRED

# uvicorn.run(
#     "main:app",
#     host = "0.0.0.0",
#     port = "5000", 
#     ssl_context = ssl_context
# )

uvicorn.run(
    "main:app",
    host = "0.0.0.0",
    port = "5000", 
    # ssl_context = ssl_context
)