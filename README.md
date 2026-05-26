# vehicle_platform
# 🚗 Site Veículos - Marketplace Django

Sistema web desenvolvido com Django para publicação e gerenciamento de anúncios de veículos, caminhões, equipamentos pesados, fazendas e animais.

---

# 📌 Funcionalidades

## 👤 Usuários

* Cadastro de usuários
* Login e logout
* Recuperação de senha
* Perfil com telefone e cidade

## 🚗 Anúncios

* Criar anúncios
* Editar anúncios
* Excluir anúncios
* Upload de múltiplas imagens
* Planos de anúncio:

  * Básico
  * Premium
  * Destaque

## 🔍 Filtros

* Filtrar por categoria
* Filtrar por fabricante
* Filtrar por modelo
* Filtrar por ano

## ❤️ Favoritos
* Adicionar anúncios aos favoritos
* Remover anúncios dos favoritos
* Página exclusiva de favoritos
* Atualização em tempo real sem reload
* Sistema AJAX para favoritar/desfavoritar

## 💰 Listings

* Venda
* Aluguel

## 📢 Sistema de planos

* Controle de expiração
* Controle de anúncios ativos
* Limite de imagens por plano

---

# 🧱 Tecnologias utilizadas

* Python 3
* Django
* SQLite
* Bootstrap
* Crispy Forms
* HTML5
* CSS3
* JavaScript

---

#

```bash
```

---

# ⚙️ Instalação

## 1. Clone o projeto

```bash
git clone https://github.com/seuusuario/site_veiculos.git
```

---

## 2. Entre na pasta

```bash
cd site_veiculos
```

---

## 3. Crie a virtualenv

### Windows

```bash
python -m venv .venv
```

---

## 4. Ative a virtualenv

### PowerShell

```bash
.\.venv\Scripts\Activate.ps1
```

---

## 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

# 🗄️ Banco de dados

## Rodar migrations

```bash
python manage.py migrate
```

---

## Criar superusuário

```bash
python manage.py createsuperuser
```

---

# ▶️ Executar projeto

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Recuperação de senha

No `settings.py` configure:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "seuemail@gmail.com"
EMAIL_HOST_PASSWORD = "senha_de_app"
```

---

# 📦 Models principais

## User

* username
* phone
* city

## Car

* categoria
* plano
* valor
* fabricante
* dono
* expiração

## Manufacturer

* fabricante do veículo

## CarImage

* imagens do anúncio

## Listing

* vendas

## Favorite
* usuário
* anúncio favorito
* data de criação

---

#

---

# 📱 Interface

* Sidebar responsiva
* Sistema de filtros automáticos
* Layout inspirado em marketplaces
* Suporte mobile

---

# 🚀 Melhorias futuras

* Login social Google
* Login WhatsApp
* API REST com DRF
* Painel administrativo avançado
* Sistema de chat entre usuários


---

# 👨‍💻 Autor

Fabio Silva

---

# 📄 Licença

Projeto para fins educacionais e comerciais.
