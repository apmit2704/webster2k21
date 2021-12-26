const driver = new Driver();

      // Define the steps for introduction
      driver.defineSteps([
        {
          // element is the thing which you want to highlight and describe and etc...
          element: '#intro',
          popover: {
            className: 'putNumber',
            title: 'Site-tour!',
            description: 'hello gamer! welcome to checkers game. lets give you a brief site-tour',
            // you can change the dialog box postition
            position: 'right'
          }
        },
        {
          element: '#side',
          popover: {
            className: 'converter-container',
            title: 'sidebar',
            description: 'click the icon to open the toggle bar for various options',
            position: 'right'
          }
        },
        {
          // element is the thing which you want to highlight and describe and etc...
          element: '#settings',
          popover: {
            className: 'putNumber',
            title: 'settings',
            description: 'you can change accordingly',
            // you can change the dialog box postition
            position: 'right'
          }
        },
        {
          // element is the thing which you want to highlight and describe and etc...
          element: '#play',
          popover: {
            className: 'putNumber',
            title: 'steps to play',
            description: 'have no idea of rules ? here you can find',
            // you can change the dialog box postition
            position: 'right'
          }
        },
        {
          // element is the thing which you want to highlight and describe and etc...
          element: '#profile',
          popover: {
            className: 'putNumber',
            title: 'profile',
            description: 'find your profile information here including you game history,rating etc',
            // you can change the dialog box postition
            position: 'right'
          }
        },
        {
          // element is the thing which you want to highlight and describe and etc...
          element: '#board',
          popover: {
            className: 'putNumber',
            title: 'Site-tour!',
            description: 'hello gamer! welcome to checkers game. lets give you a brief site-tour',
            // you can change the dialog box postition
            position: 'right'
          }
        },
        {
          element: '#brief',
          popover: {
            className: 'converter-container',
            title: 'sidebar',
            description: 'click the icon to open the toggle bar for various options',
            position: 'right'
          }
        }

      ]);

      // Start the introduction
      driver.start();