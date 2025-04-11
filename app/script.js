document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contact-form');
    const successMessage = document.getElementById('success-message');
    const newMessageBtn = document.getElementById('new-message');

    // Función para validar el formulario
    function validateForm() {
        let isValid = true;
        
        // Validar nombre
        const name = document.getElementById('name');
        const nameError = document.getElementById('name-error');
        if (name.value.trim() === '') {
            nameError.textContent = 'El nombre es obligatorio';
            isValid = false;
        } else if (name.value.trim().length < 3) {
            nameError.textContent = 'El nombre debe tener al menos 3 caracteres';
            isValid = false;
        } else {
            nameError.textContent = '';
        }
        
        // Validar email
        const email = document.getElementById('email');
        const emailError = document.getElementById('email-error');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email.value.trim() === '') {
            emailError.textContent = 'El correo electrónico es obligatorio';
            isValid = false;
        } else if (!emailRegex.test(email.value.trim())) {
            emailError.textContent = 'Por favor, introduce un correo electrónico válido';
            isValid = false;
        } else {
            emailError.textContent = '';
        }
        
        // Validar teléfono (opcional)
        const phone = document.getElementById('phone');
        const phoneError = document.getElementById('phone-error');
        const phoneRegex = /^\d{9,}$/;
        if (phone.value.trim() !== '' && !phoneRegex.test(phone.value.trim())) {
            phoneError.textContent = 'Introduce un número de teléfono válido (mínimo 9 dígitos)';
            isValid = false;
        } else {
            phoneError.textContent = '';
        }
        
        // Validar asunto
        const subject = document.getElementById('subject');
        const subjectError = document.getElementById('subject-error');
        if (subject.value === '') {
            subjectError.textContent = 'Por favor, selecciona un asunto';
            isValid = false;
        } else {
            subjectError.textContent = '';
        }
        
        // Validar mensaje
        const message = document.getElementById('message');
        const messageError = document.getElementById('message-error');
        if (message.value.trim() === '') {
            messageError.textContent = 'El mensaje es obligatorio';
            isValid = false;
        } else if (message.value.trim().length < 10) {
            messageError.textContent = 'El mensaje debe tener al menos 10 caracteres';
            isValid = false;
        } else {
            messageError.textContent = '';
        }
        
        // Validar términos
        const terms = document.getElementById('terms');
        const termsError = document.getElementById('terms-error');
        if (!terms.checked) {
            termsError.textContent = 'Debes aceptar los términos y condiciones';
            isValid = false;
        } else {
            termsError.textContent = '';
        }
        
        return isValid;
    }

    // Evento para enviar el formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validar todo el formulario al hacer submit
        if (validateForm()) {
            // Ocultar formulario y mostrar mensaje de éxito
            form.classList.add('hidden');
            successMessage.classList.remove('hidden');
        }
    });
    
    // Aplicar validaciones en tiempo real para cada campo
    const validateName = function() {
        const nameError = document.getElementById('name-error');
        const name = document.getElementById('name');
        if (name.value.trim() === '') {
            nameError.textContent = 'El nombre es obligatorio';
        } else if (name.value.trim().length < 3) {
            nameError.textContent = 'El nombre debe tener al menos 3 caracteres';
        } else {
            nameError.textContent = '';
        }
    };
    
    const validateEmail = function() {
        const emailError = document.getElementById('email-error');
        const email = document.getElementById('email');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email.value.trim() === '') {
            emailError.textContent = 'El correo electrónico es obligatorio';
        } else if (!emailRegex.test(email.value.trim())) {
            emailError.textContent = 'Por favor, introduce un correo electrónico válido';
        } else {
            emailError.textContent = '';
        }
    };
    
    const validatePhone = function() {
        const phoneError = document.getElementById('phone-error');
        const phone = document.getElementById('phone');
        const phoneRegex = /^\d{9,}$/;
        if (phone.value.trim() !== '' && !phoneRegex.test(phone.value.trim())) {
            phoneError.textContent = 'Introduce un número de teléfono válido (mínimo 9 dígitos)';
        } else {
            phoneError.textContent = '';
        }
    };
    
    const validateMessage = function() {
        const messageError = document.getElementById('message-error');
        const message = document.getElementById('message');
        if (message.value.trim() === '') {
            messageError.textContent = 'El mensaje es obligatorio';
        } else if (message.value.trim().length < 10) {
            messageError.textContent = 'El mensaje debe tener al menos 10 caracteres';
        } else {
            messageError.textContent = '';
        }
    };
    
    // Añadir event listeners para validación en tiempo real
    document.getElementById('name').addEventListener('blur', validateName);
    document.getElementById('email').addEventListener('blur', validateEmail);
    document.getElementById('phone').addEventListener('blur', validatePhone);
    document.getElementById('message').addEventListener('blur', validateMessage);
    
    // También añadir validación cuando se hace clic directamente en el botón submit
    document.querySelector('button[type="submit"]').addEventListener('click', function() {
        validateName();
        validateEmail();
        validatePhone();
        validateMessage();
        
        // Validar asunto
        const subject = document.getElementById('subject');
        const subjectError = document.getElementById('subject-error');
        if (subject.value === '') {
            subjectError.textContent = 'Por favor, selecciona un asunto';
        } else {
            subjectError.textContent = '';
        }
        
        // Validar términos
        const terms = document.getElementById('terms');
        const termsError = document.getElementById('terms-error');
        if (!terms.checked) {
            termsError.textContent = 'Debes aceptar los términos y condiciones';
        } else {
            termsError.textContent = '';
        }
    });

    // Evento para enviar un nuevo mensaje
    newMessageBtn.addEventListener('click', function() {
        // Reiniciar el formulario
        form.reset();
        
        // Limpiar todos los mensajes de error
        document.querySelectorAll('.error').forEach(function(errorElement) {
            errorElement.textContent = '';
        });
        
        // Mostrar formulario y ocultar mensaje de éxito
        form.classList.remove('hidden');
        successMessage.classList.add('hidden');
    });
});