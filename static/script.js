document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('date picker')
    var selectedDate = new Date().toISOString().split('T')[0];
    datePicker.value = selectedDate
    localStorage.setItem('selectedDate',selectedDate)
    datePicker.addEventListener('change',function() {
        selectedDate = datePicker.value; 
        console.log(selectedDate)
        localStorage.setItem('selectedDate',selectedDate)
    })
   

    // var form = document.getElementById('form')
    // form.addEventListener('submit', function(event) {
    //     var storedDate = localStorage.getItem('selectedDate');
        
    // }) 

});
