import React from 'react';
import * as echarts from 'echarts';
import geoJson from './AU';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import { makeStyles } from '@material-ui/core/styles';

const cities = [{
    name: "Melbourne",
    value: [144.946457, -37.840935, 120]
}]

const useStyles = makeStyles((theme) => ({
    root: {
        width: 300,
    },
    margin: {
        height: theme.spacing(3),
    },
}));

const loadMap = async (mapData) => {
    console.log('mapdata: ', mapData.data)
    setTimeout(() => {
        if (mapData.data.length !== 0) {
            max = mapData.data.max
            sliderMax = mapData.data.data.length
            drawMap(mapData.data.data[0])
        }
    }, 500);
}

var max = 0
var sliderMax = 0
function drawMap(data) {
    var myChart = echarts.init(document.getElementById('echartsmap'));
    echarts.registerMap('AU', geoJson);
    let option = {
        title: {
            text: 'sentiment_score',
        },
        visualMap: {
            left: 'right',
            min: 0,
            max: max,
            inRange: {
                color: ['#ffffff', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            text: ['High', 'Low'],
            calculable: true
        },
        tooltip: {},
        geo: {
            show: true,
            map: 'AU',
            label: {
                normal: { show: false },
                emphasis: { show: false }
            },
            roam: false,
            itemStyle: {
                normal: {
                    areaColor: '#47D1FF',
                    borderColor: '#3B5077'
                },
                emphasis: { areaColor: '#040404' }
            },
            zoom: 1
        },
        series: [
            {
                name: 'cities',
                type: 'scatter',
                coordinateSystem: 'geo',
                data: cities,
                symbolSize: 8,
                showEffectOn: 'emphasis',
                rippleEffect: { brushType: 'stroke' },
                hoverAnimation: true,
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'right',
                        show: true
                    },
                    emphasis: { show: true }
                },
                itemStyle: {
                    normal: { color: '#040404' }
                },
                tooltip: {
                    show: false,
                }
            },
            {
                name: 'sentiment_score',
                type: 'map',
                mapType: 'AU',
                label: {
                    show: true
                },
                data: data,
            },
        ]
    };
    myChart.setOption(option);
    myChart.hideLoading();
};

export default function Map(mapData) {
    const classes = useStyles();
    const handleChange = (event, newValue) => {
        drawMap(mapData.data.data[newValue])
    }
    loadMap(mapData)
    return (
        <div>
            <div id="echartsmap" style={{ width: '80%', height: "500px" }}></div>
            <div className={classes.root} style={{ 'margin-left': '25%' }}>
                <Typography id="discrete-slider-always" gutterBottom>
                </Typography>
                <Slider
                    defaultValue={0}
                    aria-labelledby="discrete-slider-always"
                    step={1}
                    onChange={handleChange}
                    valueLabelDisplay="on"
                    max={sliderMax - 1}
                />
            </div>
        </div>
    );
}