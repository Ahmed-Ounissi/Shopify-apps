'use client'

import { createClient } from '@supabase/supabase-js'
import { useEffect, useState } from "react"

// Initialize Supabase client
// Use your Supabase KEYS
const supabase = createClient(
  'https://oqnlcdyylcjiczmyrdoy.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9xbmxjZHl5bGNqaWN6bXlyZG95Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY2NzYwMDYsImV4cCI6MjA1MjI1MjAwNn0.bRqlB17lnb4C3nm1JJLriSmoV4K-brLCp2mWqyymtZo'
)

// Helper function to parse JSON string safely
const parseJsonField = (jsonString) => {
  try {
    return typeof jsonString === 'string' ? JSON.parse(jsonString) : []
  } catch {
    return []
  }
}

export default function Home() {
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(true)
  const [showOnlyShopifyBuilt, setShowOnlyShopifyBuilt] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [totalAppsInDB, setTotalAppsInDB] = useState(0)

  useEffect(() => {
    const fetchApps = async () => {
      try {
        // First get the total count
        const { count: totalCount } = await supabase
          .from('shopify_apps')
          .select('*', { count: 'exact', head: true })
    
        setTotalAppsInDB(totalCount)
    
        // Calculate how many pages we need
        const pageSize = 1000
        const pages = Math.ceil(totalCount / pageSize)
        let allApps = []
    
        // Fetch all pages
        for (let i = 0; i < pages; i++) {
          const { data, error } = await supabase
            .from('shopify_apps')
            .select('*')
            .range(i * pageSize, (i + 1) * pageSize - 1)
    
          if (error) throw error
          if (data) allApps = [...allApps, ...data]
        }
    
        // Process all apps
        const processedData = allApps.map(app => ({
          ...app,
          pricing_details: parseJsonField(app.pricing_details),
          languages: parseJsonField(app.languages),
          works_with: parseJsonField(app.works_with),
          categories: parseJsonField(app.categories)
        }))
    
        console.log('Total apps fetched:', processedData.length)
        setApps(processedData)
      } catch (error) {
        console.error('Error fetching apps:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchApps()
  }, [])

  // Filter apps based on search query and Shopify-built toggle
  const filteredApps = apps.filter((app) => {
    const searchLower = searchQuery.toLowerCase().trim();
    const matchesSearch =
      !searchQuery ||
      app.title?.toLowerCase().includes(searchLower) ||
      app.description?.toLowerCase().includes(searchLower) ||
      app.developer?.toLowerCase().includes(searchLower) ||
      (Array.isArray(app.categories) &&
        app.categories.some((cat) =>
          cat.toLowerCase().includes(searchLower)
        ));

    const matchesShopifyFilter =
      !showOnlyShopifyBuilt || app.is_built_for_shopify;

    return matchesSearch && matchesShopifyFilter;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-lg">Loading apps...</p>
      </div>
    )
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-blue-600 text-center mb-8">
          Shopify Apps Directory
        </h1>

        {/* Search and Filter Controls */}
        <div className="mb-8 space-y-4">
          {/* Search Input */}
          <div className="relative">
            <input
              type="text"
              placeholder="Search apps by name, description, developer, or category..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>

          {/* Filter Toggle */}
          <div className="flex justify-between items-center">
            <label className="inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={showOnlyShopifyBuilt}
                onChange={(e) => setShowOnlyShopifyBuilt(e.target.checked)}
                className="sr-only peer"
              />
              <div className="relative w-11 h-6 bg-gray-200 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              <span className="ml-3 text-sm font-medium text-gray-700">Show only built for-Shopify apps</span>
            </label>
          </div>
        </div>

        {/* Results Statistics */}
        <div className="mb-6 text-gray-600">
          <p>
            Total apps in directory: {totalAppsInDB}
          </p>
          <p>
            Showing {filteredApps.length} {filteredApps.length === 1 ? 'app' : 'apps'}
            {showOnlyShopifyBuilt ? ' built by Shopify' : ''}
            {searchQuery && ` matching "${searchQuery}"`}
          </p>
        </div>
        
        <div className="space-y-6">
          {filteredApps.map((app) => (
            <div key={app.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="p-6">
                <div className="flex items-start gap-6">
                  {app.logo_url && (
                    <div className="flex-shrink-0">
                      <img 
                        src={app.logo_url} 
                        alt={`${app.title} logo`}
                        className="w-20 h-20 object-cover rounded-lg"
                        onError={(e) => {
                          const img = e.currentTarget
                          img.onerror = null
                          img.src = '/api/placeholder/80/80'
                        }}
                      />
                    </div>
                  )}
                  
                  <div className="flex-1">
                    <div className="flex justify-between items-start flex-wrap gap-4">
                      <div>
                        <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                          {app.title}
                          {app.developer === "Shopify" && (
                            <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              Built for Shopify
                            </span>
                          )}
                        </h2>
                        {app.rating && (
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-yellow-500 font-medium">{app.rating} ★</span>
                            <span className="text-gray-600">{app.reviews ? `(${app.reviews} reviews)` : '(No reviews yet)'}</span>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex gap-3">
                        <a
                          href={app.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
                        >
                          View App
                        </a>
                        {app.developer_website && (
                          <a
                            href={app.developer_website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center px-4 py-2 bg-gray-100 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-200 transition-colors"
                          >
                            Developer Site
                          </a>
                        )}
                      </div>
                    </div>

                    <p className="text-gray-600 mt-3 mb-4">
                      {app.description || 'No description available'}
                    </p>

                    {Array.isArray(app.categories) && app.categories.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-4">
                        {app.categories.map((category, idx) => (
                          <span 
                            key={idx}
                            className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full"
                          >
                            {category}
                          </span>
                        ))}
                      </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-600">
                      {app.developer && (
                        <p><span className="font-medium">Developer:</span> {app.developer}</p>
                      )}
                      {app.developer_location && (
                        <p><span className="font-medium">Location:</span> {app.developer_location}</p>
                      )}
                      {app.launch_date && (
                        <p><span className="font-medium">Launch Date:</span> {app.launch_date}</p>
                      )}
                      {app.pricing && (
                        <p><span className="font-medium">Pricing:</span> {app.pricing}</p>
                      )}
                      {Array.isArray(app.languages) && app.languages.length > 0 && (
                        <p><span className="font-medium">Languages:</span> {app.languages.join(', ')}</p>
                      )}
                      {Array.isArray(app.works_with) && app.works_with.length > 0 && (
                        <p><span className="font-medium">Works With:</span> {app.works_with.join(', ')}</p>
                      )}
                    </div>
                    
                    {Array.isArray(app.pricing_details) && app.pricing_details.length > 0 && (
                      <div className="mt-4 border-t pt-4">
                        <h3 className="font-medium mb-2">Pricing Details:</h3>
                        <ul className="list-disc list-inside space-y-1">
                          {app.pricing_details.map((detail, idx) => (
                            <li key={idx} className="text-sm text-gray-600">{detail}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
