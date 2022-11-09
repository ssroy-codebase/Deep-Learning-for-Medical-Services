$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var formData = new FormData($('#upload-file')[0]);

        if (location.pathname.includes("Covid19")){
            formData.append('type', "Covid19");
        }
        else if (location.pathname.includes("ColonCancer")){
            formData.append('type', "ColonCancer");
        }
        else if (location.pathname.includes("LungCancer")){
            formData.append('type', "LungCancer");
        }
        else if (location.pathname.includes("Alzheimer's")){
            formData.append('type', "Alzheimer's");
        }
        else if (location.pathname.includes("BrainTumor")){
            formData.append('type', "BrainTumor");
        }
        else if (location.pathname.includes("TypeofTumor")){
            formData.append('type', "BrainTumorType");
        }
        else{
            formData.append('type', "None");
        }

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            // headers: {"Content-Type": "application/json"},
            // data: JSON.stringify(formObject),
            data: (formData),
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
            },
        });
    });

});
