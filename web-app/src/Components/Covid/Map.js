import React from 'react';
import * as echarts from 'echarts';
import geoJson from './AU';
import Typography from '@material-ui/core/Typography';
import Slider from '@material-ui/core/Slider';
import { makeStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';

const cities = [
    {
        name: "Melbourne",
        value: [144.946457, -37.840935, Infinity]
    },
    {
        name: "Sydney",
        value: [151.2093, -33.8688, Infinity]
    },
    {
        name: "Brisbane",
        value: [153.0260, -27.4705, Infinity]
    },
    {
        name: "Adelaide",
        value: [138.6007, -34.9285, Infinity]
    },
    {
        name: "Perth",
        value: [115.8613, -31.9523, Infinity]
    },
    {
        name: "Hobart",
        value: [147.3257, -42.8826, Infinity]
    },
    {
        name: "Darwin",
        value: [130.8444, -12.4637, Infinity]
    }
]

const useStyles = makeStyles((theme) => ({
    root: {
        width: 300,
    },
    margin: {
        height: theme.spacing(3),
    },
}));

const loadMap = async (mapData) => {
    setTimeout(() => {
        if (mapData.data.length !== 0) {
            mapData.data.data.forEach(item => {
                dates.push(item.date)
            })
            max = mapData.data.max_count
            sliderMax = mapData.data.data.length
            drawMap(mapData.data.data[currentValue].tweet_count_data)
        }
    }, 500);
}

var max = 0
var sliderMax = 0
var currentValue = 0
var dates = []
function drawMap(data) {
    var dom = document.getElementById('echartsmap')
    console.log(dom)
    if (dom !== null && dom !== undefined) {
        var myChart = echarts.init(dom);
        echarts.registerMap('AU', geoJson);
        let option = {
            visualMap: {
                left: 'left',
                min: 0,
                max: max * 1.2,
                inRange: {
                    color: ['#ffffff', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026', 'black']
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
                        normal: { color: 'black' }
                    },
                    tooltip: {
                        show: false,
                    }
                },
                {
                    name: '# tweets',
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
    }
    
};

function ValueLabelComponent(props) {
    const { children, open, value } = props;
  
    return (
      <Tooltip open={open} enterTouchDelay={0} placement="top" title={dates[value]}>
        {children}
      </Tooltip>
    );
  }

export default function Map(mapData) {
    const classes = useStyles();
    const handleChange = (event, newValue) => {
        currentValue = newValue
        drawMap(mapData.data.data[newValue].tweet_count_data)
    }
    loadMap(mapData)
    return (
        <div>
            <div id="echartsmap" style={{ width: '80%', height: "500px" }}></div>
            <div className={classes.root} style={{ 'margin-left': '15%' }}>
                <Typography id="discrete-slider-always" gutterBottom>
                </Typography>
                <Slider
                    defaultValue={0}
                    aria-labelledby="discrete-slider-always"
                    step={1}
                    onChange={handleChange}
                    valueLabelDisplay="on"
                    max={sliderMax - 1}
                    ValueLabelComponent={ValueLabelComponent}
                />
            </div>
        </div>
    );
}