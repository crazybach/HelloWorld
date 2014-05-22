using UnityEngine;
using System.Collections;

public class UI3DModelView : MonoBehaviour {
	
	GameObject[] models = new GameObject[2];
	
	
	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
	
	}
	
	void AddModel(GameObject obj){
		models[0] = obj;
		//obj.transform.Equals();
	}
}
