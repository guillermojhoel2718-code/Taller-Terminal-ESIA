const fs = require('fs');
const path = require('path');
const PptxGenJS = require('pptxgenjs');

// Configuración de rutas
const dataDir = path.join(__dirname, '..', 'Tesis-Urbana', '02_Datos', 'Municipios');
const outDir = path.join(__dirname, '..', 'Tesis-Urbana', '07_Outputs');
const outPath = path.join(outDir, 'Graficas_Datos_v1.pptx');

// Colores base definidos en CONTEXTO_AGENTES.md (SIN '#')
const COLORS = {
    TEPOTZOTLAN: 'C8A96E',
    TIZAYUCA: '4A7C59',
    CUAUTITLAN: 'D4441C',
    IXMIQUILPAN: '6B8FA3',
    FONDO_OSCURO: '1A1A1A',
    FONDO_CLARO: 'F5F0E8',
    FONDO_TABLA_ALT: 'EDE3D0',
    LINEAS_GRIS: 'E8E0D0',
    BLANCO: 'FFFFFF'
};

// 1. Leer los JSON
const filenames = fs.readdirSync(dataDir).filter(f => f.endsWith('.json'));
const munis = {};

filenames.forEach(f => {
    const rawData = fs.readFileSync(path.join(dataDir, f), 'utf-8');
    const data = JSON.parse(rawData);
    munis[data.municipio] = data;
});

const getMuniData = (name) => munis[name] || {};

// Instanciar PPTX y configurar Layout
let pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_16x9';

// Helper para opciones comunes de gráficos
const getChartOpts = (title) => ({
    x: 1.0, y: 1.0, w: '80%', h: '70%',
    title: title,
    titleColor: '333333',
    titleFontFace: 'Arial',
    titleFontSize: 18,
    showLegend: true,
    legendPos: 'b',
    showValue: true,
    chartArea: { fill: { color: COLORS.BLANCO }, roundedCorners: true },
    valGridLine: { color: COLORS.LINEAS_GRIS },
    catGridLine: { style: 'none' }, // Oculto
    catAxisLabelColor: "333333",
    valAxisLabelColor: "333333",
});


// ---------------------------------------------------------
// GRÁFICA 1 — Población y Densidad (Barras dobles)
// ---------------------------------------------------------
let slide1 = pptx.addSlide();
slide1.background = { color: 'FFFFFF' };

const tep = getMuniData('Tepotzotlán');
const tiz = getMuniData('Tizayuca');
const cua = getMuniData('Cuautitlán');
const ixm = getMuniData('Ixmiquilpan');

const dataChart1 = [
    {
        name: 'Población (hab)',
        labels: ['Tepotzotlán', 'Tizayuca', 'Cuautitlán', 'Ixmiquilpan'],
        values: [tep.poblacion || 0, tiz.poblacion || 0, cua.poblacion || 0, ixm.poblacion || 0]
    },
    {
        name: 'Densidad (hab/km²)',
        labels: ['Tepotzotlán', 'Tizayuca', 'Cuautitlán', 'Ixmiquilpan'],
        values: [tep.densidad_hab_km2 || 0, tiz.densidad_hab_km2 || 0, cua.densidad_hab_km2 || 0, ixm.densidad_hab_km2 || 0] // Cuautitlan 0 es tratado como visual pendiente o minimo
    }
];

let opts1 = getChartOpts('Población y Densidad');
opts1.barDir = 'col'; 
opts1.chartColors = [COLORS.IXMIQUILPAN, COLORS.TIZAYUCA]; // Colores para cada serie

slide1.addChart(pptx.ChartType.bar, dataChart1, opts1);

// Texto explicativo para Cuautitlan sin datos
slide1.addText('* Densidad Cuautitlán: [sin dato]', { x: 1.0, y: 0.5, w: 5, h: 0.5, color: '666666', fontSize: 10 });


// ---------------------------------------------------------
// GRÁFICA 2 — Conectividad Digital (Barras horizontales, ordenadas)
// ---------------------------------------------------------
let slide2 = pptx.addSlide();
slide2.background = { color: 'FFFFFF' };

// Ordenar: Cua(72.8), Tiz(54.21), Tep(48), Ixm(33.07)
const internetData = [
    { name: 'Cuautitlán', val: cua.internet_pct },
    { name: 'Tizayuca', val: tiz.internet_pct },
    { name: 'Tepotzotlán', val: tep.internet_pct },
    { name: 'Ixmiquilpan', val: ixm.internet_pct }
];

const dataChart2 = [{
    name: 'Internet %',
    labels: internetData.map(d => d.name),
    values: internetData.map(d => d.val)
}];

let opts2 = getChartOpts('Internet en Viviendas % — Clave para Teletrabajo');
opts2.barDir = 'bar';
// Destacar Ixmiquilpan en D4441C
opts2.chartColors = [COLORS.CUAUTITLAN, COLORS.IXMIQUILPAN, COLORS.TEPOTZOTLAN, COLORS.TIZAYUCA];  // Se asigna color general (por default usa el primero para la serie única)

slide2.addChart(pptx.ChartType.bar, dataChart2, opts2);

// ---------------------------------------------------------
// GRÁFICA 3 — Pobreza y Rezago Social
// ---------------------------------------------------------
let slide3 = pptx.addSlide();
slide3.background = { color: 'FFFFFF' };

const dataChart3 = [
    {
        name: 'Pobreza %',
        labels: ['Ixmiquilpan', 'Tepotzotlán', 'Tizayuca', 'Cuautitlán'],
        values: [ixm.pobreza_pct, tep.pobreza_pct, tiz.pobreza_pct, cua.pobreza_pct]
    },
    {
        name: 'Rezago Educativo %',
        labels: ['Ixmiquilpan', 'Tepotzotlán', 'Tizayuca', 'Cuautitlán'],
        values: [ixm.rezago_educativo_pct, tep.rezago_educativo_pct, tiz.rezago_educativo_pct, cua.rezago_educativo_pct]
    }
];

let opts3 = getChartOpts('Pobreza y Rezago Social');
opts3.barDir = 'bar';
opts3.chartColors = [COLORS.TIZAYUCA, COLORS.TEPOTZOTLAN];

slide3.addChart(pptx.ChartType.bar, dataChart3, opts3);


// ---------------------------------------------------------
// GRÁFICA 4 — Servicios Básicos
// ---------------------------------------------------------
let slide4 = pptx.addSlide();
slide4.background = { color: 'FFFFFF' };

const dataChart4 = [
    {
        name: 'Agua Potable %',
        labels: ['Tepotzotlán', 'Tizayuca', 'Cuautitlán', 'Ixmiquilpan'],
        values: [tep.agua_pct||0, tiz.agua_pct||0, 0, ixm.agua_pct||0]
    },
    {
        name: 'Drenaje %',
        labels: ['Tepotzotlán', 'Tizayuca', 'Cuautitlán', 'Ixmiquilpan'],
        values: [tep.drenaje_pct||0, tiz.drenaje_pct||0, 0, ixm.drenaje_pct||0]
    },
    {
        name: 'Electricidad %',
        labels: ['Tepotzotlán', 'Tizayuca', 'Cuautitlán', 'Ixmiquilpan'],
        values: [tep.electricidad_pct||0, tiz.electricidad_pct||0, 0, ixm.electricidad_pct||0]
    }
];

let opts4 = getChartOpts('Servicios Básicos');
opts4.barDir = 'col';
opts4.barGrouping = 'clustered';
opts4.chartColors = [COLORS.TEPOTZOTLAN, COLORS.IXMIQUILPAN, COLORS.TIZAYUCA];

slide4.addChart(pptx.ChartType.bar, dataChart4, opts4);
slide4.addText('* Cuautitlán: [PEND.] en todos los servicios básicos', { x: 1.0, y: 0.5, w: 8, h: 0.5, color: '666666', fontSize: 10 });


// ---------------------------------------------------------
// GRÁFICA 5 — Tabla Comparativa
// ---------------------------------------------------------
let slide5 = pptx.addSlide();
slide5.background = { color: 'FFFFFF' };

const formatVal = (val) => val === null || val === undefined ? '[PEND.]' : val.toString();

const keys = [
    "poblacion", "superficie_km2", "densidad_hab_km2", "internet_pct", 
    "pobreza_pct", "rezago_educativo_pct", "agua_pct"
];

// Row 1 (Header)
const tableData = [
    [
        { text: 'Indicador', options: { fill: COLORS.FONDO_OSCURO, color: COLORS.TEPOTZOTLAN, bold: true } },
        { text: 'Tepotzotlán', options: { fill: COLORS.FONDO_OSCURO, color: COLORS.TEPOTZOTLAN, bold: true } },
        { text: 'Tizayuca', options: { fill: COLORS.FONDO_OSCURO, color: COLORS.TEPOTZOTLAN, bold: true } },
        { text: 'Cuautitlán', options: { fill: COLORS.FONDO_OSCURO, color: COLORS.TEPOTZOTLAN, bold: true } },
        { text: 'Ixmiquilpan', options: { fill: COLORS.FONDO_OSCURO, color: COLORS.TEPOTZOTLAN, bold: true } }
    ]
];

// Content Rows
keys.forEach((key, index) => {
    let fill = index % 2 === 0 ? COLORS.FONDO_CLARO : COLORS.FONDO_TABLA_ALT;
    tableData.push([
        { text: key, options: { fill: fill, color: '333333' } },
        { text: formatVal(tep[key]), options: { fill: fill, color: '333333' } },
        { text: formatVal(tiz[key]), options: { fill: fill, color: '333333' } },
        { text: formatVal(cua[key]), options: { fill: fill, color: '333333' } },
        { text: formatVal(ixm[key]), options: { fill: fill, color: '333333' } }
    ]);
});

slide5.addTable(tableData, { x: 0.5, y: 1.0, w: '90%', fontSize: 12, border: { pt: 1, color: COLORS.LINEAS_GRIS } });
slide5.addText('Tabla Comparativa de Indicadores Base', { x: 0.5, y: 0.3, w: '90%', fontSize: 18, color: '333333', bold: true });


// ---------------------------------------------------------
// EXPORTACION
// ---------------------------------------------------------
pptx.writeFile({ fileName: outPath })
    .then(fileName => {
        console.log(`PPTX generado exitosamente: ${fileName}`);
    })
    .catch(err => {
        console.error("Error al generar PPTX", err);
    });

