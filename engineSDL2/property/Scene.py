
import threading

import Golem
import property

class Scene(property.SpriteGroup):
    def __init__(self, t_window, t_id):
        property.SpriteGroup.__init__(self)
        self.sceneId = t_id
        self.sceneName = ""
        self.window = t_window
        
    def setSceneName(self, name):
        self.sceneName = name
        return self
        
    def setSceneId(self, t_id):
        self.id = t_id
        return self
        
class SceneHandler():
    def __init__(self, t_window, default_scene = None):
    
        self.window = t_window
        
        self.m_scenes = {
            0: default_scene if default_scene else Scene(self.window, 0),
        }
        
        self.currentSceneId = 0
        self.m_currentScene = self.m_scenes[self.currentSceneId]
        
        self.sceneRenderLock = threading.Lock()
        self.sceneDrawLock = threading.Lock()
        self.sceneUpdateLock = threading.Lock()
        
        self.nextId = 1
        
    def __del__(self):
        pass
        
#    def add(self, spr):
#        self.m_currentScene.add(spr)
        
    def remove(self, spr):
        if self.m_currentScene.contains(spr):
            self.m_currentScene.remove(spr)
        
    def render(self):
         
        self.sceneRenderLock.acquire()
        if self.m_currentScene: self.m_currentScene.render()
        self.sceneRenderLock.release()
        
    def update(self):
        self.sceneUpdateLock.acquire()
        if self.m_currentScene: self.m_currentScene.update()
        self.sceneUpdateLock.release()
        
    def draw(self, surface):
        if surface: 
            self.sceneDrawLock.acquire()
            
            if self.m_currentScene: self.m_currentScene.draw(surface)
            
            self.sceneDrawLock.release()
        
        else: 
            print("Error: SceneHandler:: Surface is None")
    
    def add(self, t_sprite):
        if self.m_currentScene: self.m_currentScene.add(t_sprite)
    
    def addTo(self, spr, scene_number):
        
        self.m_scenes[scene_number].add(spr)
        
    def removeFrom(self, spr, scene_number):
        
        self.m_scenes[scene_number].remove(spr)
        
    def handleEvent(self, e):
    
        self.sceneUpdateLock.acquire()
        
        if self.m_currentScene: self.m_currentScene.handleEvent(e)
        self.sceneUpdateLock.release()
        
    def createScene(self, sceneClass = Scene):
        i = -1
        if self.nextId not in self.m_scenes:
            #self.sceneLock.acquire()
            self.sceneRenderLock.acquire()
            self.sceneDrawLock.acquire()
            self.sceneUpdateLock.acquire()
            self.m_scenes[self.nextId] = sceneClass(self.window, self.nextId)
            self.nextId +=1 # Need not be under lock protect.
            i = self.nextId - 1
            #self.sceneLock.release()
            self.sceneUpdateLock.release()
            self.sceneDrawLock.release()
            self.sceneRenderLock.release()
            
        return i
        
    def switchScene(self, sceneId):
        if self.currentSceneId == sceneId or sceneId not in self.m_scenes:
            return
        
        self.sceneRenderLock.acquire()
        self.sceneDrawLock.acquire()
        self.sceneUpdateLock.acquire()
        
        self.m_currentScene = self.m_scenes[sceneId]
        self.currentSceneId = sceneId
        
        self.sceneUpdateLock.release()
        self.sceneDrawLock.release()
        self.sceneRenderLock.release()

    def sprites(self):
        return self.m_currentScene.sprites() if self.m_currentScene != None else []
