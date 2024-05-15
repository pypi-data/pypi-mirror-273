# MeliAPIClient

Este módulo permite interactuar con el API de mercado libre para leer, actualizar y crear productos y órdenes. Este módulo es útil para integrar el API de Mercado libre con otros sistemas.

## Instalación

Para instalar este módulo, ejecute el siguiente comando:

```bash
pip install MeliAPIClient
```

### Uso básico

Para usar este módulo, debemos guardar las credenciales en 3 archivos tipo JSON. El archivo `ml_keys` almacena el `client_id` y `client_secret`, `ml_token` almacena la información para renovar la sesión después del límite de 6 horas, y `ml_user` que almacena la información del usuario, donde el dato más importante es el ID del usuario.

```python
from MeliAPIClient import Session
from MeliAPIClient import Order


def run():

    session = Session("ml_keys.json", 'ml_token.json', "ml_user.json")
    orders = Order(session)

    orders.list(year=2024, month=5)


if __name__ == "__main__":
    run()
```

## Créditos

Camilo Andrés Rodriguez

## referencias

https://developers.mercadolibre.com/

## Licencia

Este proyecto está bajo la Licencia [MIT].
