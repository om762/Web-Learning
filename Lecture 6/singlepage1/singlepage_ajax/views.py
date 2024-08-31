from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Index Page
def index(request):
    return render(request, "index.html")


state_of_matters = {
    "solid":"In a solid, constituent particles (ions, atoms, or molecules) are closely packed together. The forces between particles are so strong that the particles cannot move freely but can only vibrate. As a result, a solid has a stable, definite shape, and a definite volume. Solids can only change their shape by an outside force, as when broken or cut. In crystalline solids, the particles (atoms, molecules, or ions) are packed in a regularly ordered, repeating pattern. There are various different crystal structures, and the same substance can have more than one structure (or solid phase). For example, iron has a body-centred cubic structure at temperatures below 912 °C (1,674 °F), and a face-centred cubic structure between 912 and 1,394 °C (2,541 °F). Ice has fifteen known crystal structures, or fifteen solid phases, which exist at various temperatures and pressures. Glasses and other non-crystalline, amorphous solids without long-range order are not thermal equilibrium ground states; therefore they are described below as nonclassical states of matter. Solids can be transformed into liquids by melting, and liquids can be transformed into solids by freezing. Solids can also change directly into gases through the process of sublimation, and gases can likewise change directly into solids through deposition.",
    "liquid": "A liquid is a nearly incompressible fluid that conforms to the shape of its container but retains a (nearly) constant volume independent of pressure. The volume is definite if the temperature and pressure are constant. When a solid is heated above its melting point, it becomes liquid, given that the pressure is higher than the triple point of the substance. Intermolecular (or interatomic or interionic) forces are still important, but the molecules have enough energy to move relative to each other and the structure is mobile. This means that the shape of a liquid is not definite but is determined by its container. The volume is usually greater than that of the corresponding solid, the best known exception being water, H2O. The highest temperature at which a given liquid can exist is its critical temperature.",
    "gas": "A gas is a compressible fluid. Not only will a gas conform to the shape of its container but it will also expand to fill the container. In a gas, the molecules have enough kinetic energy so that the effect of intermolecular forces is small (or zero for an ideal gas), and the typical distance between neighboring molecules is much greater than the molecular size. A gas has no definite shape or volume, but occupies the entire container in which it is confined. A liquid may be converted to a gas by heating at constant pressure to the boiling point, or else by reducing the pressure at constant temperature. At temperatures below its critical temperature, a gas is also called a vapor, and can be liquefied by compression alone without cooling. A vapor can exist in equilibrium with a liquid (or solid), in which case the gas pressure equals the vapor pressure of the liquid (or solid). A supercritical fluid (SCF) is a gas whose temperature and pressure are above the critical temperature and critical pressure respectively. In this state, the distinction between liquid and gas disappears. A supercritical fluid has the physical properties of a gas, but its high density confers solvent properties in some cases, which leads to useful applications. For example, supercritical carbon dioxide is used to extract caffeine in the manufacture of decaffeinated coffee."
}

def state_response(request, state_of_matter):
    if state_of_matter == "home":
        return HttpResponse("")
    if state_of_matter in state_of_matters.keys():
        return HttpResponse(state_of_matters[state_of_matter])
    else:
        return HttpResponse("State not found.")