        // Add your JavaScript code here

        $(document).ready(function () {
            // After the page has loaded, show the body and schedule full-screen display
            $('body').fadeIn('slow', function () {
                setTimeout(showFullScreen, 5000); // Show full-screen after 3 seconds
            });
        });

        function showFullScreen() {
            // Show the full-screen content
            $('body').css('display', 'block');
        }