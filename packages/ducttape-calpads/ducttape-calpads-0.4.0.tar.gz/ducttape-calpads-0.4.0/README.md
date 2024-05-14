# ducttape-calpads
An extension to the ducttape package for automating common tasks in California Department of Education's CALPADS system.

### Installing
Because this is an extension of the [ducttape package](https://github.com/SummitPublicSchools/ducttape), we also need to set up a proper Chrome + Selenium environment before installing `ducttape-calpads`:
- Set up a Chrome + Selenium environment on your computer. Instructions [here](https://medium.com/@patrick.yoho11/installing-selenium-and-chromedriver-on-windows-e02202ac2b08).
- We currently use tags on GitHub for versioning. You can check [the releases](https://github.com/SummitPublicSchools/ducttape-calpads/releases) to find the latest release version or find older versions. To install a release in your preferred environment, we recommend running: 
    - `pip install git+https://github.com/SummitPublicSchools/ducttape-calpads.git@v0.4.0` (you can set the `@v0.4.0` to a preferred version, i.e. `@version_tag`.)
