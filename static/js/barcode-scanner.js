/**
 * Sistema de Leitor de Código de Barras Avançado
 * Suporta câmera, leitores físicos e entrada manual
 */

class BarcodeScanner {
    constructor() {
        this.codeReader = null;
        this.stream = null;
        this.isScanning = false;
        this.barcodeBuffer = '';
        this.barcodeTimeout = null;
        
        this.initElements();
        this.bindEvents();
    }
    
    initElements() {
        this.codigoBarrasField = document.getElementById('id_codigo_barras');
        this.scanButton = document.getElementById('scanButton');
        this.manualButton = document.getElementById('manualInput');
        this.stopScanButton = document.getElementById('stopScan');
        this.scannerDiv = document.getElementById('scanner');
        this.instructionsDiv = document.getElementById('instructions');
        this.videoElement = document.createElement('video');
        
        // Configurar vídeo
        this.videoElement.style.width = '100%';
        this.videoElement.style.height = '100%';
        this.videoElement.style.objectFit = 'cover';
        this.videoElement.setAttribute('playsinline', true);
    }
    
    bindEvents() {
        if (!this.codigoBarrasField) return;
        
        // Auto-busca produto
        this.codigoBarrasField.addEventListener('input', (e) => this.handleInput(e));
        
        // Botões
        this.scanButton?.addEventListener('click', () => this.startCamera());
        this.manualButton?.addEventListener('click', () => this.showManualInput());
        this.stopScanButton?.addEventListener('click', () => this.stopScanning());
        
        // Detectar leitor físico
        document.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Feedback visual
        this.codigoBarrasField.addEventListener('focus', () => this.handleFocus());
        this.codigoBarrasField.addEventListener('blur', () => this.handleBlur());
        
        // Auto-focus inicial
        this.codigoBarrasField.focus();
    }
    
    handleInput(e) {
        clearTimeout(this.inputTimeout);
        const codigo = e.target.value.trim();
        
        if (codigo.length >= 8) {
            this.inputTimeout = setTimeout(() => {
                this.buscarProduto(codigo);
            }, 500);
        }
    }
    
    handleKeydown(e) {
        if (document.activeElement !== this.codigoBarrasField) return;
        
        clearTimeout(this.barcodeTimeout);
        
        if (e.key === 'Enter') {
            e.preventDefault();
            if (this.barcodeBuffer.length >= 8) {
                this.codigoBarrasField.value = this.barcodeBuffer;
                this.buscarProduto(this.barcodeBuffer);
            }
            this.barcodeBuffer = '';
            return;
        }
        
        if (e.key.length === 1) {
            this.barcodeBuffer += e.key;
            this.barcodeTimeout = setTimeout(() => {
                this.barcodeBuffer = '';
            }, 100);
        }
    }
    
    handleFocus() {
        this.codigoBarrasField.style.borderColor = '#007bff';
        this.codigoBarrasField.style.backgroundColor = '#fff';
        this.codigoBarrasField.style.boxShadow = '0 0 10px rgba(0, 123, 255, 0.3)';
    }
    
    handleBlur() {
        this.codigoBarrasField.style.borderColor = '#ddd';
        this.codigoBarrasField.style.backgroundColor = '#f9f9f9';
        this.codigoBarrasField.style.boxShadow = 'none';
    }
    
    async startCamera() {
        try {
            this.scannerDiv.style.display = 'block';
            const interactive = document.getElementById('interactive');
            interactive.innerHTML = '';
            interactive.appendChild(this.videoElement);
            
            // Solicitar câmera
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: 'environment',
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });
            
            this.videoElement.srcObject = this.stream;
            await this.videoElement.play();
            
            // Inicializar ZXing
            if (typeof ZXing !== 'undefined') {
                this.codeReader = new ZXing.BrowserMultiFormatReader();
                this.isScanning = true;
                
                this.codeReader.decodeFromVideoDevice(null, this.videoElement, (result, err) => {
                    if (result && this.isScanning) {
                        const code = result.getText();
                        if (code && code.length >= 8) {
                            this.processScannedCode(code);
                        }
                    }
                    if (err && !(err instanceof ZXing.NotFoundException)) {
                        console.error('Erro no scanner:', err);
                    }
                });
            }
            
        } catch (error) {
            console.error('Erro ao acessar câmera:', error);
            this.showError('❌ Erro ao acessar a câmera. Use o modo manual.');
            this.scannerDiv.style.display = 'none';
        }
    }
    
    processScannedCode(code) {
        this.codigoBarrasField.value = code;
        this.stopScanning();
        this.buscarProduto(code);
        this.showSuccess('📱 Código escaneado: ' + code);
    }
    
    showManualInput() {
        this.instructionsDiv.style.display = 'block';
        this.codigoBarrasField.focus();
        this.codigoBarrasField.select();
    }
    
    stopScanning() {
        this.isScanning = false;
        
        if (this.codeReader) {
            this.codeReader.reset();
            this.codeReader = null;
        }
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.videoElement.srcObject = null;
        this.scannerDiv.style.display = 'none';
    }
    
    async buscarProduto(codigo) {
        try {
            const response = await fetch('/buscar-produto-por-codigo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({codigo_barras: codigo})
            });
            
            const data = await response.json();
            
            if (data.encontrado) {
                this.preencherFormulario(data);
                this.showSuccess('✅ Produto encontrado: ' + data.nome);
            } else {
                this.showInfo('ℹ️ Produto não encontrado. Cadastre um novo produto.');
            }
            
            document.getElementById('id_nome').focus();
            
        } catch (error) {
            console.error('Erro ao buscar produto:', error);
            this.showError('❌ Erro ao buscar produto.');
            document.getElementById('id_nome').focus();
        }
    }
    
    preencherFormulario(data) {
        const campos = {
            'id_nome': data.nome,
            'id_preco': data.preco,
            'id_descricao': data.descricao || '',
            'id_fornecedor': data.fornecedor || '',
            'id_unidade': data.unidade,
            'id_observacao': data.observacao || ''
        };
        
        Object.entries(campos).forEach(([id, valor]) => {
            const elemento = document.getElementById(id);
            if (elemento && valor) {
                elemento.value = valor;
            }
        });
    }
    
    showSuccess(message) {
        this.showNotification(message, 'success');
    }
    
    showError(message) {
        this.showNotification(message, 'error');
    }
    
    showInfo(message) {
        this.showNotification(message, 'info');
    }
    
    showNotification(message, type = 'info') {
        // Criar notificação temporária
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            max-width: 300px;
            word-wrap: break-word;
            ${type === 'success' ? 'background: #28a745;' : ''}
            ${type === 'error' ? 'background: #dc3545;' : ''}
            ${type === 'info' ? 'background: #17a2b8;' : ''}
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new BarcodeScanner();
});