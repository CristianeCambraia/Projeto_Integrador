# 🎥 Como Testar a Câmera

## 1. **Teste Básico**
Abra o arquivo `teste_camera.html` no navegador:
```
file:///C:/Users/crist/OneDrive/Área de Trabalho/Projeto_Integrador/teste_camera.html
```

## 2. **Problemas Comuns**

### ❌ **Câmera não abre**
- **Causa**: Navegador bloqueia câmera em HTTP
- **Solução**: Use HTTPS ou localhost

### ❌ **Permissão negada**
- **Causa**: Usuário negou acesso
- **Solução**: Clique no ícone 🔒 na barra de endereços → Permitir câmera

### ❌ **Navegador não suporta**
- **Causa**: Navegador muito antigo
- **Solução**: Use Chrome, Firefox ou Edge atualizados

## 3. **Teste no Django**

### Inicie o servidor:
```bash
cd "C:\Users\crist\OneDrive\Área de Trabalho\Projeto_Integrador"
python manage.py runserver
```

### Acesse:
```
http://127.0.0.1:8000/produtos/cadastrar/
```

## 4. **Alternativas se Câmera não Funcionar**

### ✅ **Modo Manual**
- Clique no botão ✏️
- Digite o código manualmente
- Pressione Enter

### ✅ **Leitor Físico**
- Conecte leitor USB
- Clique no campo de código
- Escaneie normalmente

### ✅ **App do Celular**
- Use app "Barcode Scanner"
- Escaneie o código
- Copie e cole no campo

## 5. **Códigos de Teste**
Use estes códigos para testar:
- `7891000100103` (Coca-Cola)
- `7896029013724` (Nescau)
- `7891000053508` (Leite Ninho)

---

## 🔧 **Se Ainda Não Funcionar**

O sistema tem **3 métodos** de entrada:
1. 📷 Scanner por câmera
2. 🔌 Leitor físico USB/Bluetooth  
3. ✏️ Entrada manual

**Pelo menos um sempre funcionará!**