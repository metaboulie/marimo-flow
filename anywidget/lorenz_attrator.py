import marimo

__generated_with = "0.8.15"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return mo,


@app.cell(hide_code=True)
def __():
    import anywidget
    import traitlets


    class LorenzSystemWidget(anywidget.AnyWidget):
        _esm = """
        import p5 from 'https://cdn.skypack.dev/p5';

        function render({ model, el }) {
            // Initial positions for the three nodes
            let x1 = 0.01, y1 = -0.2, z1 = 1;
            let x2 = -0.01, y2 = 0.2, z2 = 1.5;

            // Lorenz system parameters for each node
            const params1 = { a: 10, b: 28, c: 8.0 / 3.0 };
            const params2 = { a: 10, b: 28, c: 8.0 / 3.0 };

            // Arrays to store the trajectory points of each node
            let points1 = [];
            let points2 = [];

            // Arrays to store the trajectory points for sub-visualizations
            let points1XY = [];
            let points1XZ = [];
            let points1YZ = [];
            let points2XY = [];
            let points2XZ = [];
            let points2YZ = [];

            new p5((p) => {
                p.setup = () => {
                    let canvas = p.createCanvas(800, 800, p.WEBGL);
                    canvas.style('visibility', 'visible')
                    canvas.parent(el);
                    p.colorMode(p.RGB);
                    p.background(0);
                    p.noFill();
                };

                p.draw = () => {
                    p.background(0, 0, 0, 50);

                    const dt = 0.01;

                    // Update first node
                    const dx1 = (params1.a * (y1 - x1)) * dt;
                    const dy1 = (x1 * (params1.b - z1) - y1) * dt;
                    const dz1 = (x1 * y1 - params1.c * z1) * dt;
                    x1 += dx1;
                    y1 += dy1;
                    z1 += dz1;
                    points1.push(p.createVector(x1, y1, z1));
                    points1XY.push(p.createVector(x1, y1, 0));
                    points1XZ.push(p.createVector(x1, 0, z1));
                    points1YZ.push(p.createVector(0, y1, z1));

                    // Update second node
                    const dx2 = (params2.a * (y2 - x2)) * dt;
                    const dy2 = (x2 * (params2.b - z2) - y2) * dt;
                    const dz2 = (x2 * y2 - params1.c * z2) * dt;
                    x2 += dx2;
                    y2 += dy2;
                    z2 += dz2;
                    points2.push(p.createVector(x2, y2, z2));
                    points2XY.push(p.createVector(x2, y2, 0));
                    points2XZ.push(p.createVector(x2, 0, z2));
                    points2YZ.push(p.createVector(0, y2, z2));

                    // Camera setup
                    const camX = 250 * p.cos(p.frameCount * 0.01);
                    const camY = 250 * p.sin(p.frameCount * 0.01);
                    const camZ = 700 + 150 * p.sin(p.frameCount * 0.005);
                    p.camera(camX, camY, camZ, 0, 0, 0, 0, 1, 0);

                    p.scale(5);
                    p.strokeWeight(2);

                    // Draw first node trajectory
                    p.stroke(255, 127, 80);
                    p.beginShape();
                    for (let v of points1) {
                        p.vertex(v.x, v.y, v.z);
                    }
                    p.endShape();

                    // Draw second node trajectory
                    p.stroke(186, 85, 211);
                    p.beginShape();
                    for (let v of points2) {
                        p.vertex(v.x, v.y, v.z);
                    }
                    p.endShape();

                    // Draw sub-visualizations
                    p.push();
                    p.scale(0.5);
                    p.strokeWeight(0.5);
                    p.stroke(255, 127, 80);
                    p.beginShape();
                    for (let v of points1XY) {
                        p.vertex(v.x - 100, v.y - 100);
                    }
                    p.endShape();
                    p.stroke(186, 85, 211);
                    p.beginShape();
                    for (let v of points2XY) {
                        p.vertex(v.x - 100, v.y - 100);
                    }
                    p.endShape();
                    p.pop();

                    p.push();
                    p.scale(0.5);
                    p.strokeWeight(0.5);
                    p.stroke(255, 127, 80);
                    p.beginShape();
                    for (let v of points1XZ) {
                        p.vertex(v.x - 100, v.z);
                    }
                    p.endShape();
                    p.stroke(186, 85, 211);
                    p.beginShape();
                    for (let v of points2XZ) {
                        p.vertex(v.x - 100, v.z);
                    }
                    p.endShape();
                    p.pop();

                    p.push();
                    p.scale(0.5);
                    p.strokeWeight(0.5);
                    p.stroke(255, 127, 80);
                    p.beginShape();
                    for (let v of points1YZ) {
                        p.vertex(v.z - 100, v.y - 50);
                    }
                    p.endShape();
                    p.stroke(186, 85, 211);
                    p.beginShape();
                    for (let v of points2YZ) {
                        p.vertex(v.z - 100, v.y - 50);
                    }
                    p.endShape();
                    p.pop();

                    // Limit the number of points to prevent memory issues
                    if (points1.length > 1000) {
                        points1.shift();
                        points1XY.shift();
                        points1XZ.shift();
                        points1YZ.shift();
                    }
                    if (points2.length > 1000) {
                        points2.shift();
                        points2XY.shift();
                        points2XZ.shift();
                        points2YZ.shift();
                    }
                };
            });
        }
            export default { render }
        """

        value = traitlets.Int(0).tag(sync=True)
    return LorenzSystemWidget, anywidget, traitlets


@app.cell(hide_code=True)
def __(LorenzSystemWidget, mo):
    lorenz_system_widget = mo.ui.anywidget(LorenzSystemWidget())
    lorenz_system_widget.center()
    return lorenz_system_widget,


if __name__ == "__main__":
    app.run()
