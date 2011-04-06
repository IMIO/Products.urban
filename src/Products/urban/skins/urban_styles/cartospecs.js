        //Ext.BLANK_IMAGE_URL = 's.gif';
        
	var map, toolbar;
        var infolayername = "portionouts";
	
	var  sketchSymbolizers = {
                "Point": {
                    pointRadius: 4,
                    graphicName: "square",
                    fillColor: "white",
                    fillOpacity: 1,
                    strokeWidth: 1,
                    strokeOpacity: 1,
                    strokeColor: "#333333"
                },
                "Line": {
                    strokeWidth: 3,
                    strokeOpacity: 1,
                    strokeColor: "#666666",
                    strokeDashstyle: "dash"
                },
                "Polygon": {
                    strokeWidth: 2,
                    strokeOpacity: 1,
                    strokeColor: "#666666",
                    fillColor: "white",
                    fillOpacity: 0.3
                }
	};
	
	var storeCouche = new Ext.data.SimpleStore({
	  fields: ['layerName', 'commonName'],
	  data : [
			  ['portionouts', 'Parcelles'],
			  ['CharleroiDemo', 'Toutes'],
			  ['affect', 'Plan de secteur'],
			  ['buildings', 'Bati']
		   ]
	});

	function setHTML(response) {
		
		if ( response.responseText != "")
		{
			var g =  new OpenLayers.Format.GML_GFI();
			  htmlt = ""
			  var features = g.read(response.responseText);
			  for(var feat in features) {
				if ( features[feat].layerName )
				{
				    htmlt += "<p><h1>Couche: "+ features[feat].layerName+"</h1> <br><table border='1' cellpadding='5' class='listing'>";
				    passe = false;
				    for (var j in features[feat].features) {
					if ( passe == false ) {
						htmlt += "<tr>";
						for (var m in features[feat].features[j].attributes) {
							htmlt += "<th> " + m +"</th>";
						}
						htmlt += "</tr>";
						passe= true;
					}
					htmlt += "<tr>";
					for (var m in features[feat].features[j].attributes) {
						htmlt += "<td>"+features[feat].features[j].attributes[m]+"</td>";
					}
					htmlt += "</tr>"
				    }
				    htmlt += "</p></table><br>"
				}
			  } 
		  }
		
		var nav = new Ext.Panel
		({
		    title: 'Navigation',
		    html: htmlt,
		     header: false,
	            border: false
		});

		var win = new Ext.Window
		({
		    title: 'Layout Window',
		    closable:true,
		    modal: true,
		    plain:true,
		    items: [nav ]
		});
		win.show();
	}
	
	 function handleMeasurements(event) {
            var geometry = event.geometry;
            var units = event.units;
            var order = event.order;
            var measure = event.measure;
           
            var out = "";
            if(order == 1) {
                out += "" + measure.toFixed(3) + " " + units;
            } else {
                out += "" + measure.toFixed(3) + " " + units + "<sup>2</" + "sup>";
            }
	    Ext.MessageBox.alert('Résultat : ',out);
        }

	
	function addSeparator(toolbar){
            toolbar.add(new Ext.Toolbar.Spacer());
            toolbar.add(new Ext.Toolbar.Separator());
            toolbar.add(new Ext.Toolbar.Spacer());
        } 

        function initToolbarContent() {
            toolbar.addControl(
                new OpenLayers.Control.ZoomToMaxExtent({
                    map: map,
                    title: 'Zoom to maximum map extent'
                }), {
                    iconCls: 'zoomfull', 
                    toggleGroup: 'map'
                }
            );
            
            addSeparator(toolbar);
        
            toolbar.addControl(
                new OpenLayers.Control.ZoomBox({
                    title: 'Zoom in: click in the map or use the left mouse button and drag to create a rectangle'
                }), {
                    iconCls: 'zoomin', 
                    toggleGroup: 'map'
                }
            );
        
            toolbar.addControl(
                new OpenLayers.Control.ZoomBox({
                    out: true,
                    title: 'Zoom out: click in the map or use the left mouse button and drag to create a rectangle'
                }), {
                    iconCls: 'zoomout', 
                    toggleGroup: 'map'
                }
            );
            
            toolbar.addControl(
                new OpenLayers.Control.DragPan({
                    isDefault: true,
                    title: 'Pan map: keep the left mouse button pressed and drag the map'
                }), {
                    iconCls: 'pan', 
                    toggleGroup: 'map'
                }
            );
	    
	    var style = new OpenLayers.Style();
            style.addRules([
                new OpenLayers.Rule({symbolizer: sketchSymbolizers})
            ]);
            var styleMap = new OpenLayers.StyleMap({"default": style});
            
            var options = {
                handlerOptions: {
                    style: "default", // this forces default render intent
                    layerOptions: {styleMap: styleMap},
                    persist: true
                }
            };
	    var mesurectl = new OpenLayers.Control.Measure(OpenLayers.Handler.Path,options);
	    mesurectl.events.on({
			//"measurepartial": handleMeasurements,
                    "measure": handleMeasurements
	    });

	    toolbar.addControl(mesurectl ,
		{
                    iconCls: 'drawline', 
                    toggleGroup: 'map'
                }
            );

            addSeparator(toolbar);

            var nav = new OpenLayers.Control.NavigationHistory();
            map.addControl(nav);
            nav.activate();
            
            toolbar.add(
                new Ext.Toolbar.Button({
                    iconCls: 'back',
                    tooltip: 'Previous view', 
                    handler: nav.previous.trigger
                })
            );
            
            toolbar.add(
                new Ext.Toolbar.Button({
                    iconCls: 'next',
                    tooltip: 'Next view', 
                    handler: nav.next.trigger
                })
            );
            
            addSeparator(toolbar);
	    var cb = new Ext.form.ComboBox({
		  store: storeCouche,
		  displayField:'commonName',
		  valueField:'layerName',
		  mode: 'local',
		  triggerAction: 'all',
		  emptyText:'Séléctionnez une couche ...',

		  listeners: {
			'select': {
				fn: function() {
					infolayername = cb.getValue();
				}
			}
		  }
	    });
	    toolbar.add(
		cb
	    );
            toolbar.activate();
        }


		OpenLayers.IMAGE_RELOAD_ATTEMPTS = 5;
		OpenLayers.DOTS_PER_INCH = 25.4 / 0.28;
        
		
                
