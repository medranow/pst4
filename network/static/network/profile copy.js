
document.addEventListener('DOMContentLoaded', function() {
    console.log('hi');
    

    document.querySelectorAll('.buttonProfile').forEach(function(buttonProfile) {
        buttonProfile.onclick = function () {
            
            document.querySelector('.post_view').style.display = 'none';
            }
        });
    });
