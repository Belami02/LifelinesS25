import reflex as rx
from chat.components.mainNavbar import mainNavbar

def map():
    return rx.vstack(
        rx.box(id="map-container", width="780px", height="400px"),
        rx.script(
            """
            function loadBingMap() {
                var existingScript = document.querySelector("script[src*='bing.com/api/maps']");
                if (existingScript) {
                    existingScript.remove(); // Remove old script to force reload
                }

                var script = document.createElement("script");
                script.type = "text/javascript";
                script.src = "http://www.bing.com/api/maps/mapcontrol?callback=GetMap";
                script.async = true;
                script.defer = true;
                document.body.appendChild(script);
            }

            function GetMap() {
                var map = new Microsoft.Maps.Map(document.getElementById('map-container'), {
                    credentials: 'AmF4N_XOzIVDhyRmDUgmfYVN_Ezcr1suvebkSQNfXFXMWY88acIl7AqY1gMDMk_8',
                    center: new Microsoft.Maps.Location(40.773091, -73.988285),
                    zoom: 14
                });

                var infobox = new Microsoft.Maps.Infobox(map.getCenter(), { visible: false });
                infobox.setMap(map);

                var pins = [
                    { lat: 40.788091, lon: -73.968285, title: 'Lost Golden Retriever', desc: 'I lost my golden retriever near Central Park. Please help!' },
                    { lat: 40.75750, lon: -73.99167, title: 'Lost iPhone', desc: 'I lost my iPhone in the subway on the way to 42nd Street. It’s a black iPhone 13 with a cracked screen. If you find it, please contact me!' },
                    { lat: 40.773998, lon: -73.966003, title: 'Found Black Cat in Downtown', desc: 'I found a black cat near the intersection of 5th Avenue and Main Street. The cat is friendly and seems to be an indoor pet.' }
                ];

                pins.forEach(pinData => {
                    var pin = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(pinData.lat, pinData.lon), { title: pinData.title, text: '1' });
                    pin.metadata = { title: pinData.title, description: pinData.desc };
                    Microsoft.Maps.Events.addHandler(pin, 'click', function (e) {
                        infobox.setOptions({ location: e.target.getLocation(), title: e.target.metadata.title, description: e.target.metadata.description, visible: true });
                    });
                    map.entities.push(pin);
                });
            }

            loadBingMap();
            """
        ),
    )

def MapPage():
    return rx.vstack(
        mainNavbar(),
        map(),
        align_items="center",
        spacing="8"
    )