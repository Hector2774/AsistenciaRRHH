document.addEventListener('DOMContentLoaded', function() {
    const btnValidar = document.getElementById('btn-validar');
    
    btnValidar.addEventListener('click', function() {
        const sucursalId = document.getElementById('sucursal').value;
        const fecha = document.getElementById('fecha').value;
        
        if (!fecha) {
            alert('Por favor selecciona una fecha');
            return;
        }
        
        btnValidar.disabled = true;
        btnValidar.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validando...';
        
        // Configurar CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch('/marcaje/validar-asistencia/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `sucursal=${sucursalId}&fecha=${fecha}`
        })
        .then(response => {
            console.log('Status:', response.status); // ← Agrega esto
            console.log('Content-Type:', response.headers.get('content-type')); // ← Y esto
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) }); // ← Muestra el error real
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            const tbody = document.querySelector('#tabla-resultados tbody');
            tbody.innerHTML = '';
            
            data.data.forEach(empleado => {
                const row = document.createElement('tr');
                if (!empleado.asistio) {
                    row.classList.add('table-danger');
                }
                
                row.innerHTML = `
                    <td>${empleado.codigo}</td>
                    <td>${empleado.nombre}</td>
                    <td>${empleado.sucursal}</td>
                    <td>
                        ${empleado.asistio 
                            ? '<span class="badge bg-success">Asistió</span>' 
                            : '<span class="badge bg-danger">Falta</span>'}
                    </td>
                `;
                
                tbody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        })
        .finally(() => {
            btnValidar.disabled = false;
            btnValidar.innerHTML = '<i class="fas fa-check-circle"></i> Validar';
        });
    });
});

