import reflex as rx
from chat.components.mainNavbar import mainNavbar

def map():
    return rx.card(
        rx.html(
        """
	<head>
		<meta charset="utf-8"/>
		<link rel="stylesheet" type="text/css" href="css/style.css">
	    <script type='text/javascript' 
            src='http://www.bing.com/api/maps/mapcontrol?callback=GetMap' 
            async defer></script>
	</head>

	<body>
		<div id="container">
			<div class="row">
				<div>
					<div id="exampleMap" style="position:relative; width:1000px; height:700px;"></div>
				</div>
			</div>
		</div>
		<script type='text/javascript'>
			function GetMap() {
				var map = new Microsoft.Maps.Map('#exampleMap', {
					credentials: 'AmF4N_XOzIVDhyRmDUgmfYVN_Ezcr1suvebkSQNfXFXMWY88acIl7AqY1gMDMk_8',
					center: new Microsoft.Maps.Location(40.773091, -73.988285),zoom: 14
				});	
				var infobox = new Microsoft.Maps.Infobox(map.getCenter(), {
					visible: false
				});

				infobox.setMap(map);
				var center = map.getCenter();
				var pin1 = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(40.788091, -73.968285), {
					title: 'Lost Golden Retriever',
					subTitle: 'Central Park',
					text: '1'
				});
                pin1.metadata = {
                    title: 'Lost Golden Retriever',
                    description: 'I lost my golden retriever near Central Park. Please help!'
                };	
                
                var pin2 = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(40.75750, -73.99167), {
					title: 'Lost iPhone',
					subTitle: '42nd Street',
					text: '1'
				});
                pin2.metadata = {
                    title: 'Lost iPhone',
                    description: 'I lost my iPhone in the subway on the way to 42nd Street. It’s a black iPhone 13 with a cracked screen. If you find it, please contact me!'
                };	
                
                var pin3 = new Microsoft.Maps.Pushpin(new Microsoft.Maps.Location(40.773998, -73.966003), {
					title: 'Found Black Cat in Downtown',
					subTitle: '5th Avenue',
					text: '1'
				});
                pin3.metadata = {
                    title: 'Found Black Cat in Downtown',
                    description: 'I found a black cat near the intersection of 5th Avenue and Main Street in downtown. The cat is in great condition and appears to be well-fed and well-cared for. It has a shiny coat and green eyes. The cat is very friendly and seems to be an indoor pet as it is comfortable with people and other pets.'
                };		

                Microsoft.Maps.Events.addHandler(pin1, 'click', pushpinClicked);
                Microsoft.Maps.Events.addHandler(pin2, 'click', pushpinClicked);
                Microsoft.Maps.Events.addHandler(pin3, 'click', pushpinClicked);
                    
                map.entities.push(pin1);	
                map.entities.push(pin2);
                map.entities.push(pin3);		
                function pushpinClicked(e) {
                    if (e.target.metadata) {
                        infobox.setOptions({
                            location: e.target.getLocation(),title: e.target.metadata.title,
                            description: e.target.metadata.description, visible: true
                        });
                    }
                }
			}   
			</script>
		
	</body>

        """
        ),
        max_width="1200px",
        background_color="var(--gray-2)",
    )

def MapPage():
    return rx.vstack(
        mainNavbar(),
        map(),
        align_items="center",
        spacing="8"
    )
