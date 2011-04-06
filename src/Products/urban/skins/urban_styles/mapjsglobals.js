        var map, layer;

            // style the sketch fancy
            var sketchSymbolizers = {
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
            var style = new OpenLayers.Style();
            style.addRules([
                new OpenLayers.Rule({symbolizer: sketchSymbolizers})
            ]);
            var styleMap = new OpenLayers.StyleMap({"default": style});

    function ShowMeasure(event){
        var geometry = event.geometry;
            var units = event.units;
            var order = event.order;
            var measure = event.measure;
            
            var out = "";
            if(order == 1) {
                out += "Mesure: " + measure.toFixed(3) + " " + units;
            } else {
                out += "Mesure: " + measure.toFixed(3) + " " + units + "2";
            }
        alert(out);
    }

        function buildMapParcelleUrl(select) {
        if(select != null && select.features != null && select.features.length > 0)
        {
            var idList = [];
            //var msg = "Confirmer la selection des parcelles suivantes: \r\n";
            var url = "parcelsinfo?";
                for(i = 0; i < select.features.length; i++)
            {
                idList.push(select.features[i].attributes["capakey"]);
                    url += "capakey=" + select.features[i].attributes["capakey"]+"&";
            }
            parent.frames["prcinfosframe"].window.location=url;
            
        }
    }
