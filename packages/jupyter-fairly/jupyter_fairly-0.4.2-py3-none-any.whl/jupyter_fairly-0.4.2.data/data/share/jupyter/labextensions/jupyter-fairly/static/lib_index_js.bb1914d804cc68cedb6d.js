"use strict";
(self["webpackChunkjupyter_fairly"] = self["webpackChunkjupyter_fairly"] || []).push([["lib_index_js"],{

/***/ "./lib/dataset.js":
/*!************************!*\
  !*** ./lib/dataset.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cloneDatasetCommandPlugin: () => (/* binding */ cloneDatasetCommandPlugin),
/* harmony export */   createDatasetCommandPlugin: () => (/* binding */ createDatasetCommandPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _widgets_CloneForm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets/CloneForm */ "./lib/widgets/CloneForm.js");






// import { logger } from './logger';
// import { Level } from './tokens';
function initDataset(path, template) {
    /**
     * Initializes a Fairly dataset
     * @param path - path to dataset root directory. Default to current path
     * @param template - alias of template for manifest.yalm
     */
    // name of the template for manifest.yalm
    let templateMeta = '';
    /* ./ is necessary becaucause defaultBrowser.Model.path
    * returns an empty string when fileBlowser is on the
    * jupyterlab root directory
    */
    let rootPath = './';
    if (template === '4TU.Research' || template === 'Figshare') {
        templateMeta = 'figshare';
    }
    else if (template === 'Zenodo') {
        templateMeta = 'zenodo';
    }
    else if (template == null || template === 'Default') {
        templateMeta = 'default';
    }
    console.log(rootPath.concat(path));
    (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('newdataset', {
        method: 'POST',
        body: JSON.stringify({
            path: rootPath.concat(path),
            template: templateMeta
        })
    })
        .then(data => {
        console.log(data);
    })
        .catch(reason => {
        console.error(`${reason}`);
        // show error when manifest.yalm already exist in rootPath
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error: Has the dataset been initilized already?", reason);
    });
}
function cloneDataset(source, destination, extract = false, client) {
    /**
     * clones a remote dataset to a directory
     * @param source - DOI or URL to the remote dataset
     * @param destination - realtive path to a directory to store the dataset
     * @param client - fairly client
     */
    /* ./ is necessary becaucause defaultBrowser.Model.path
    * returns an empty string when fileBlowser is on the
    * jupyterlab root directory
    */
    let rootPath = './';
    let _client = '4tu';
    let payload = JSON.stringify({
        source: source,
        destination: rootPath.concat(destination),
        extract: extract,
        client: _client
    });
    console.log(rootPath.concat(destination));
    // notification
    const delegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
    const complete = "complete";
    const failed = "failed";
    (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('clone', {
        method: 'POST',
        body: payload
    })
        .then(data => {
        console.log(data);
        delegate.resolve({ complete });
    })
        .catch(reason => {
        delegate.reject({ failed });
        // show error when destination directory is not empty
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)("Error when cloning dataset", reason);
    });
    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.promise(delegate.promise, {
        pending: { message: 'Cloning dataset...', options: { autoClose: false } },
        success: {
            message: (result) => `Clonning ${result.complete}.`,
            options: { autoClose: 3000 }
        },
        error: { message: () => `Cloning failed.` }
    });
}
const cloneDatasetCommandPlugin = {
    id: '@jupyter-fairly/clone',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, fileBrowserFactory) => {
        const fileBrowser = fileBrowserFactory.tracker.currentWidget;
        const fileBrowserModel = fileBrowser.model;
        const cloneDatasetCommand = "cloneDataset";
        app.commands.addCommand(cloneDatasetCommand, {
            label: 'Clone Dataset',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.downloadIcon,
            execute: async () => {
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: 'Clone Dataset',
                    body: new _widgets_CloneForm__WEBPACK_IMPORTED_MODULE_5__.FairlyCloneForm(),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: 'Cancel' }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Clone' })
                    ],
                    checkbox: {
                        label: 'Extract compressed files',
                        caption: 'Uncompress zip and tar.gz files',
                        checked: false
                    }
                });
                if (result.button.accept && result.value) {
                    try {
                        cloneDataset(result.value, fileBrowserModel.path, result.isChecked);
                        console.log('accepted');
                        await fileBrowserModel.refresh();
                    }
                    catch (error) {
                        console.error('Encontered an error when cloning the dataset: ', error);
                    }
                    ;
                }
                else {
                    console.log('rejected');
                }
            }
        });
        app.contextMenu.addItem({
            command: cloneDatasetCommand,
            // matches anywhere in the filebrowser
            selector: '.jp-DirListing-content',
            rank: 103
        });
    }
};
const createDatasetCommandPlugin = {
    id: '@jupyter-fairly/create-dataset',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, fileBrowserFactory) => {
        const fileBrowser = fileBrowserFactory.tracker.currentWidget;
        const fileBrowserModel = fileBrowser.model;
        const createDatasetCommand = "createDatasetCommand";
        app.commands.addCommand(createDatasetCommand, {
            label: 'Create Fairly Dataset',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.addIcon,
            execute: async () => {
                // return relative path w.r.t. jupyter root path.
                // root-path = empty string.
                console.log(`the path is: ${fileBrowserModel.path}`);
                let metadataTemplate = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getItem({
                    title: 'Select template for dataset\'s metadata',
                    items: ['', 'Default', '4TU.Research', 'Zenodo', 'Figshare'],
                    okLabel: 'Create',
                });
                // initialize dataset when accept button is clicked and 
                // vaule for teamplate is not null
                if (metadataTemplate.button.accept && metadataTemplate.value) {
                    console.log(`the path is: ${fileBrowserModel.path}`);
                    initDataset(fileBrowserModel.path, metadataTemplate.value);
                    await fileBrowserModel.refresh();
                }
                else {
                    console.log('rejected');
                    return;
                }
            }
        });
        app.contextMenu.addItem({
            command: createDatasetCommand,
            // matches anywhere in the filebrowser
            selector: '.jp-DirListing-content',
            rank: 100
        });
    }
};


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyter-fairly', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _dataset__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./dataset */ "./lib/dataset.js");
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./metadata */ "./lib/metadata.js");
/* harmony import */ var _upload__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./upload */ "./lib/upload.js");
/* harmony import */ var _menu__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./menu */ "./lib/menu.js");





/**
 *  Activate jupyter-fairly extension.
 */
const plugin = {
    id: '@jupyter-fairly:plugin',
    autoStart: true,
    requires: [],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry],
    activate: (app) => {
        console.log('JupyterLab extension jupyter-fairly is activated!');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    plugin,
    _dataset__WEBPACK_IMPORTED_MODULE_1__.createDatasetCommandPlugin,
    _metadata__WEBPACK_IMPORTED_MODULE_2__.editMetadataPlugin,
    _upload__WEBPACK_IMPORTED_MODULE_3__.uploadDatasetPlugin,
    _dataset__WEBPACK_IMPORTED_MODULE_1__.cloneDatasetCommandPlugin,
    _menu__WEBPACK_IMPORTED_MODULE_4__.FairlyMenuPlugin,
]);


/***/ }),

/***/ "./lib/menu.js":
/*!*********************!*\
  !*** ./lib/menu.js ***!
  \*********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FairlyMenuPlugin: () => (/* binding */ FairlyMenuPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");


// Icons



function registerToken(repository, newToken) {
    /**
     * register token to fairly configuration file
     * @param repository- name of data repository
     * @param newToken - access token for data repository
     */
    var clientId;
    if (repository === '4TU.ResearchData') {
        clientId = '4tu';
    }
    else if (repository === 'Zenodo') {
        clientId = 'zenodo';
    }
    else if (repository === 'Figshare') {
        clientId = 'figshare';
    }
    ;
    let payload = JSON.stringify({
        client: clientId,
        token: newToken
    });
    (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('repo-token', {
        method: 'POST',
        body: payload
    })
        .then(data => {
        console.log(data);
        // show notification when requestAPI succeeds
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.success('Access Token registered successfully.', { autoClose: 3000 });
    })
        .catch(reason => {
        // show error when requestAPI fails
        // TODO: show error message in notification, and add reason as callback()
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Error when registering access token", reason);
    });
}
;
/**
* Initialization data for the main menu example.
*/
const FairlyMenuPlugin = {
    id: '@jupyter-fairly/mainmenu',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory],
    autoStart: true,
    activate: (app) => {
        console.log("registerTokenPlugin activated!!");
        const registerTokenCommand = 'registerAccessToken';
        app.commands.addCommand(registerTokenCommand, {
            label: 'Add Repository Token',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.settingsIcon,
            execute: async () => {
                // Asks for the data repository
                let targetRepository = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getItem({
                    title: 'Register Access Token. Select Data Repository',
                    items: ['4TU.ResearchData', 'Zenodo', 'Figshare'],
                    okLabel: 'Continue',
                });
                if (targetRepository.button.accept && targetRepository.value) {
                    // Asks for the access token
                    let accessToken = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({
                        title: 'Enter Access Token for: '.concat(targetRepository.value),
                        placeholder: 'Access Token',
                        okLabel: 'Add Token',
                    });
                    if (accessToken.button.accept) {
                        console.log('registering token');
                        registerToken(targetRepository.value, accessToken.value);
                    }
                    else {
                        console.log('operation was canceled by the user');
                        return;
                    }
                    ;
                }
                else {
                    console.log('canceled');
                    return;
                }
                ;
            }
        });
        const openURLCommand = 'fairly:openURL';
        app.commands.addCommand(openURLCommand, {
            label: 'Fairly Documentation',
            caption: 'Fairly Documentation',
            execute: (args) => {
                window.open(`${args['url']}`, '_blank');
            }
        });
    }
};


/***/ }),

/***/ "./lib/metadata.js":
/*!*************************!*\
  !*** ./lib/metadata.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   editMetadataPlugin: () => (/* binding */ editMetadataPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);



const editMetadataPlugin = {
    id: '@jupyter-fairly/metadata',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, fileBrowserFactory) => {
        const fileBrowser = fileBrowserFactory.tracker.currentWidget;
        const fileBrowserModel = fileBrowser.model;
        // Open the manifest.yalm file in the file editor
        const openManifestCommand = "openManifestCommand";
        app.commands.addCommand(openManifestCommand, {
            label: 'Edit Dataset Metadata',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.editIcon,
            execute: () => {
                let currentPath = './'.concat(fileBrowserModel.path);
                const pathManifest = currentPath.concat('/manifest.yaml');
                /* We assume that the current directory contains the
                manifest.yalm, if not we show an error message
                 */
                try {
                    fileBrowserModel.manager.open(pathManifest);
                }
                catch (error) {
                    // TODO: customize error type
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)("Error Opening manifest.yalm", error);
                }
                ;
            }
        });
        app.contextMenu.addItem({
            command: openManifestCommand,
            // matches anywhere in the filebrowser
            selector: '.jp-DirListing-content',
            rank: 101
        });
    }
};


/***/ }),

/***/ "./lib/upload.js":
/*!***********************!*\
  !*** ./lib/upload.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   uploadDatasetPlugin: () => (/* binding */ uploadDatasetPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");



// Icons



function uploadDataset(directory, repository) {
    /**
     * upload local dataset to data reposotory
     * @param directory - realtive path to directory of local dataset
     * @param repository - name of data repository
     */
    /* ./ is necessary becaucause defaultBrowser.Model.path
    * returns an empty string when fileBlowser is on the
    * jupyterlab root directory
    */
    let rootPath = './';
    var client;
    if (repository === '4TU.ResearchData') {
        client = '4tu';
    }
    else if (repository === 'Zenodo') {
        client = 'zenodo';
    }
    else if (repository === 'Figshare') {
        client = 'figshare';
    }
    ;
    let payload = JSON.stringify({
        directory: rootPath.concat(directory),
        client: client
    });
    // notification
    const delegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
    const complete = "complete";
    const failed = "failed";
    (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('upload', {
        method: 'POST',
        body: payload
    })
        .then(data => {
        console.log(data);
        delegate.resolve({ complete });
    })
        .catch(reason => {
        delegate.reject({ failed });
        // show error when 
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Error when uploading dataset", reason);
    });
    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.promise(delegate.promise, {
        pending: { message: 'Uploading dataset...', options: { autoClose: false } },
        success: {
            message: (result) => `Dataset upload ${result.complete}.`,
            options: { autoClose: 3000 }
        },
        error: { message: () => `Upload failed.` }
    });
}
;
function pushDataset(localDataset) {
    /**
     * upload local dataset to data reposotory
     * @param localDataset - realtive path to directory of local dataset with remote metadata
     */
    /* ./ is necessary becaucause defaultBrowser.Model.path
    * returns an empty string when fileBlowser is on the
    * jupyterlab root directory
    */
    let rootPath = './';
    let payload = JSON.stringify({
        localdataset: rootPath.concat(localDataset)
    });
    // notification
    const delegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
    const complete = "complete";
    const failed = "failed";
    (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('push', {
        method: 'PATCH',
        body: payload
    })
        .then(data => {
        console.log(data);
        delegate.resolve({ complete });
    })
        .catch(reason => {
        delegate.reject({ failed });
        // show error when 
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)("Error when updating remote dataset", reason);
    });
    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.promise(delegate.promise, {
        pending: { message: 'Pushing dataset to repository ...', options: { autoClose: false } },
        success: {
            message: (result) => `Remote dataset update ${result.complete}.`,
            options: { autoClose: 3000 }
        },
        error: { message: () => `Pushing has failed.` }
    });
}
;
const uploadDatasetPlugin = {
    id: '@jupyter-fairly/upload',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, fileBrowserFactory) => {
        console.log("uploadDatasetPlugin activated!!");
        // const fileBrowser = fileBrowserFactory.defaultBrowser;
        const fileBrowser = fileBrowserFactory.tracker.currentWidget;
        const fileBrowserModel = fileBrowser.model;
        // ** Upload a new dataset to a data repository **
        const uploadDatasetCommand = "uploadDataset";
        app.commands.addCommand(uploadDatasetCommand, {
            label: 'Upload Dataset',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.fileUploadIcon,
            execute: async () => {
                // return relative path w.r.t. jupyterlab root path.
                // root-path = empty string.
                let targetRepository = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getItem({
                    title: 'Select Data Repository',
                    items: ['4TU.ResearchData', 'Zenodo', 'Figshare'],
                    okLabel: 'Continue',
                });
                // initialize dataset when accept button is clicked and 
                // vaule for teamplate is not null
                if (targetRepository.button.accept && targetRepository.value) {
                    let confirmAction = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getBoolean({
                        title: 'Do you want to upload the dataset?',
                        label: `Yes, upload metadata and files to ${targetRepository.value}`
                    });
                    if (confirmAction.button.accept) {
                        console.log('uploading dataset');
                        uploadDataset(fileBrowserModel.path, targetRepository.value);
                    }
                    else {
                        console.log('do not archive');
                        return;
                    }
                    ;
                }
                else {
                    console.log('rejected');
                    return;
                }
            }
        });
        // ** Push changes made to a local dataset to a data repository **
        const pushCommand = "pushDataset";
        app.commands.addCommand(pushCommand, {
            label: 'Push',
            isEnabled: () => true,
            isVisible: () => true,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.redoIcon,
            execute: async () => {
                let confirmAction = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: 'Push changes',
                    body: 'This will update the data repository using changes made here.',
                    host: document.body,
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Push' })],
                });
                if (confirmAction.button.accept) {
                    await pushDataset(fileBrowserModel.path);
                }
                else {
                    console.log('rejected');
                    return;
                }
                ;
            }
        });
        app.contextMenu.addItem({
            command: uploadDatasetCommand,
            // matches anywhere in the filebrowser
            selector: '.jp-DirListing-content',
            rank: 104
        });
        app.contextMenu.addItem({
            command: pushCommand,
            // matches anywhere in the filebrowser
            selector: '.jp-DirListing-content',
            rank: 105
        });
    }
};


/***/ }),

/***/ "./lib/widgets/CloneForm.js":
/*!**********************************!*\
  !*** ./lib/widgets/CloneForm.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FairlyCloneForm: () => (/* binding */ FairlyCloneForm)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The UI for the form fields shown within the Clone modal.
 */
class FairlyCloneForm extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Creates a form for cloning datasets
     *
     */
    constructor() {
        super({ node: FairlyCloneForm.createFormNode() });
    }
    /**
     * Returns the input value as plain text
     */
    getValue() {
        // TODO: this should be properly initialized, 
        // See: https://stackoverflow.com/questions/40349987/how-to-suppress-error-ts2533-object-is-possibly-null-or-undefined
        return this.node.querySelector('input').value.trim(); // strickNullChecks = true, brakes this code
    }
    static createFormNode() {
        const node = document.createElement('div');
        const label = document.createElement('label');
        const input = document.createElement('input');
        const text = document.createElement('span');
        node.className = 'jp-RedirectForm';
        text.textContent = 'Enter URL or DOI: ';
        input.placeholder = 'https://doi.org/xx.x/xx.vx';
        label.appendChild(text);
        label.appendChild(input);
        node.appendChild(label);
        return node;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.bb1914d804cc68cedb6d.js.map