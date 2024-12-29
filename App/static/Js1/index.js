
    // Select all the carousels
    const carousels = ['#carouselExampleInterval1', '#carouselExampleInterval2', '#carouselExampleInterval3'];

    // Function to control all carousels
    function controlCarousels(action) {
        carousels.forEach(carouselId => {
            const carousel = new bootstrap.Carousel(document.querySelector(carouselId));
            if (action === 'prev') {
                carousel.prev();
            } else if (action === 'next') {
                carousel.next();
            }
        });
    }

    // Previous button click event
    document.getElementById('prevButton').addEventListener('click', function() {
        controlCarousels('prev');
    });

    // Next button click event
    document.getElementById('nextButton').addEventListener('click', function() {
        controlCarousels('next');
    });

