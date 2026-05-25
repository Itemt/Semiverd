/**
 * app.js
 * Punto de entrada principal de la aplicación Semiverd MVC.
 */

import { StateModel } from './models/state.js';
import { MainView } from './views/mainView.js';
import { LoginView } from './views/loginView.js';
import { HomeView } from './views/homeView.js';
import { TreeView } from './views/treeView.js';
import { MapView } from './views/mapView.js';
import { MissionView } from './views/missionView.js';
import { AcademiaView } from './views/academiaView.js';
import { RankingView } from './views/rankingView.js';
import { PerfilView } from './views/perfilView.js';
import { AppController } from './controllers/appController.js';

window.addEventListener('DOMContentLoaded', () => {
  // Instanciar Modelo (State)
  const model = new StateModel();

  // Instanciar Vistas (Views)
  const views = {
    mainView: new MainView(),
    loginView: new LoginView(),
    homeView: new HomeView(),
    treeView: new TreeView(),
    mapView: new MapView(),
    missionView: new MissionView(),
    academiaView: new AcademiaView(),
    rankingView: new RankingView(),
    perfilView: new PerfilView()
  };

  // Instanciar Controlador (Controller)
  const controller = new AppController(model, views);

  // Exponer a window para compatibilidad con handlers inline del HTML
  window.mostrarTab = (tab) => views.loginView.mostrarTab(tab);
  window.activarCamara = () => controller.activarCamara();
  window.capturarFoto = () => controller.capturarFoto();
  window.loginFacial = () => controller.ejecutarLoginFacial();
  window.loginCorreo = () => controller.ejecutarLoginCorreo();
  window.registrarUsuario = () => controller.ejecutarRegistro();
  window.loginDemo = () => controller.ejecutarDemo();
  window.irA = (route) => controller.irA(route);
  window.cerrarSesion = () => controller.cerrarSesion();
  window.toggleSidebar = () => views.mainView.toggleSidebar();
  window.cerrarModalMision = () => views.missionView.cerrarModal();
  window.filtrarTips = () => {}; // Ya manejado por addEventListener en el controller

  // Inicializar controlador (arranca tema, sesión, manejadores de eventos, etc.)
  controller.inicializar();
});
