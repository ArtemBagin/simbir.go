from routers import (
    admin_account,
    admin_rent,
    admin_transport,
    auth,
    paymant,
    rent,
    transports,
    users,
)

routers = (
    auth.router,
    users.router,
    admin_account.router,
    paymant.router,
    transports.router,
    admin_transport.router,
    rent.router,
    admin_rent.router
)
