# 🗄️ CONFIGURAR BANCO DE DADOS PERMANENTE

## ❌ PROBLEMA ATUAL
- Cada deploy apaga todos os dados (usuários, orçamentos, produtos, etc.)
- SQLite é resetado a cada nova versão
- Dados não ficam permanentes

## ✅ SOLUÇÃO: PostgreSQL Permanente

### 1️⃣ BACKUP REALIZADO
✅ Backup dos dados atuais salvo em: `backup_dados.json`
- 6 Usuários
- 7 Clientes  
- 5 Fornecedores
- 23 Produtos
- 12 Orçamentos (incluindo Fernando Campos)
- 2 Admins

### 2️⃣ CONFIGURAR NO RENDER.COM

#### A) Criar Banco PostgreSQL
1. Acesse https://render.com
2. Faça login na sua conta
3. Clique em "New +" → "PostgreSQL"
4. Configure:
   - **Name**: `insumed-database`
   - **Database**: `insumed_db`
   - **User**: `insumed_user`
   - **Region**: `Oregon (US West)`
   - **PostgreSQL Version**: `15`
   - **Plan**: `Free` (0$/mês)
5. Clique em "Create Database"

#### B) Obter URL de Conexão
1. Após criar, clique no banco criado
2. Na aba "Info", copie a **Internal Database URL**
3. Exemplo: `postgresql://insumed_user:senha@dpg-xxx-a.oregon-postgres.render.com/insumed_db`

#### C) Configurar no Web Service
1. Vá para seu Web Service no Render
2. Clique em "Environment"
3. Adicione a variável:
   - **Key**: `DATABASE_URL`
   - **Value**: Cole a URL copiada acima
4. Clique em "Save Changes"

### 3️⃣ FAZER DEPLOY
1. Faça commit das alterações:
```bash
git add .
git commit -m "Configurado banco PostgreSQL permanente"
git push origin master
```

2. O Render fará deploy automático

### 4️⃣ RESTAURAR DADOS
Após o deploy com PostgreSQL:

1. Acesse o terminal do Render ou execute localmente:
```bash
python manage.py migrate
python restaurar_dados.py
```

### 5️⃣ VERIFICAR
- Acesse o sistema
- Verifique se todos os dados estão lá
- Teste criar novos orçamentos
- Faça um novo deploy para confirmar que os dados permanecem

## 🎯 RESULTADO ESPERADO
✅ Dados permanentes entre deploys
✅ Orçamentos de Fernando Campos sempre visíveis
✅ Usuários não precisam se recadastrar
✅ Produtos e fornecedores mantidos

## 📞 SUPORTE
Se houver problemas:
1. Verifique se a DATABASE_URL está correta
2. Confirme que o banco PostgreSQL está ativo
3. Execute as migrações: `python manage.py migrate`
4. Restaure os dados: `python restaurar_dados.py`

## ⚠️ IMPORTANTE
- O backup está em `backup_dados.json` - NÃO DELETE este arquivo
- Mantenha a URL do banco segura
- O plano Free do PostgreSQL tem limite de 1GB